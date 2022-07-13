#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"
#define PROTOCOL_ERROR_CHECK "ec"

#define PROTOCOL_FROM "fr"
#define PROTOCOL_TO "to"

#define PROTOCOL_FORWARD "f"
#define PROTOCOL_BACKWARD "b"
#define PROTOCOL_GET_SWITCHES_INFO "gsi"
#define PROTOCOL_STEP_DELAY "sd"
#define PROTOCOL_MOTOR_INDEX "i"
#define PROTOCOL_N_PULSES "n"
#define PROTOCOL_LIMINARY_STEP_DELAY "lsd"
#define PROTOCOL_LIMINARY_N_PULSES "ln"
#define PROTOCOL_STOP "stop"

#define PROTOCOL_LIMIT_REACHED "lrc"
#define PROTOCOL_LIMIT_RELEASED "lrl"
#define PROTOCOL_LIMIT_REMAINING_STEPS "lrs"
#define PROTOCOL_MOVE_COMPLETED "mc"
#define PROTOCOL_LIMIT_DIRECTION "ld"
#define PROTOCOL_LIMIT_DIRECTION_FORWARD "f"
#define PROTOCOL_LIMIT_DIRECTION_BACKWARD "b"

#define PROTOCOL_ELECTROMAGNET "e"
#define PROTOCOL_MAGNETIZE "m"

#define RPI_SERIAL Serial
#define DYNAMIXEL_RADIUS_WRIST_SERIAL Serial2
#define DYNAMIXEL_THUMB_SERIAL Serial3

String receivedEvent = "";
String dynamixelRadiusWristReceivedEvent = "";
String dynamixelThumbReceivedEvent = "";
DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));

unsigned long currentMicros = 0;

#define N_MOTORS 3
byte motorStepPins[N_MOTORS] = {2, 3, 4};
byte motorDirPins[N_MOTORS] = {8, 9, 10};
unsigned long motorLiminaryStepDelays[N_MOTORS] = {1500, 1500, 1500};
unsigned long motorStepDelays[N_MOTORS] = {1500, 1500, 1500};
unsigned long motorCurrentStepDelays[N_MOTORS] = {1500, 1500, 1500};
unsigned long motorPreviousMicros[N_MOTORS] = {0, 0, 0};
int motorLiminaryNPulses[N_MOTORS] = {0, 0, 0};
int motorAccelerationNPulses[N_MOTORS] = {0, 0, 0};
int motorNPulses[N_MOTORS] = {0, 0, 0};
int motorDecelerationNPulses[N_MOTORS] = {0, 0, 0};
#define NO_PIN -1
int motorForwardLimitSwitchPin[N_MOTORS] = {NO_PIN, 26, 28};
bool motorForwardLimitSwitchLastRead[N_MOTORS] = {false, false, false};
int motorBackwardLimitSwitchPin[N_MOTORS] = {24, NO_PIN, NO_PIN};
bool motorBackwardLimitSwitchLastRead[N_MOTORS] = {false, false, false};

#define ELECTROMAGNET_PIN 52

void setMotorForward(int motorIndex) {
  digitalWrite(motorDirPins[motorIndex], HIGH);
}

void setMotorBackward(int motorIndex) {
  digitalWrite(motorDirPins[motorIndex], LOW);
}

void sendMoveCompletedEvent(int motorIndex) {
    StaticJsonDocument<JSON_OBJECT_SIZE(2)> moveCompletedEvent;
    moveCompletedEvent[PROTOCOL_CATEGORY] = PROTOCOL_MOVE_COMPLETED;
    moveCompletedEvent[PROTOCOL_MOTOR_INDEX] = motorIndex;
    serializeJson(moveCompletedEvent, Serial);
    Serial.println();
}

void sendLimitReachedEvent(int motorIndex, String direction, int remainingSteps) {
    StaticJsonDocument<JSON_OBJECT_SIZE(5)> limitReachedEvent;
    limitReachedEvent[PROTOCOL_CATEGORY] = PROTOCOL_LIMIT_REACHED;
    limitReachedEvent[PROTOCOL_MOTOR_INDEX] = motorIndex;
    limitReachedEvent[PROTOCOL_LIMIT_DIRECTION] = direction;
    limitReachedEvent[PROTOCOL_LIMIT_REMAINING_STEPS] = remainingSteps;
    serializeJson(limitReachedEvent, Serial);
    Serial.println();
}

void sendLimitReleasedEvent(int motorIndex, String direction, int remainingSteps) {
    StaticJsonDocument<JSON_OBJECT_SIZE(5)> limitReleasedEvent;
    limitReleasedEvent[PROTOCOL_CATEGORY] = PROTOCOL_LIMIT_RELEASED;
    limitReleasedEvent[PROTOCOL_MOTOR_INDEX] = motorIndex;
    limitReleasedEvent[PROTOCOL_LIMIT_DIRECTION] = direction;
    limitReleasedEvent[PROTOCOL_LIMIT_REMAINING_STEPS] = remainingSteps;
    serializeJson(limitReleasedEvent, Serial);
    Serial.println();
}

bool isLimitSwitchPressed(int pin) {
    if (pin == NO_PIN) {
        return false;
    }

    // Limit switches are INPUT_PULLUP pins, so 0 means the switch is triggered
    return !digitalRead(pin);
}

void setup() {
  RPI_SERIAL.begin(9600);
  DYNAMIXEL_RADIUS_WRIST_SERIAL.begin(9600);
  DYNAMIXEL_THUMB_SERIAL.begin(9600);

  pinMode(ELECTROMAGNET_PIN, OUTPUT);
  digitalWrite(ELECTROMAGNET_PIN, LOW);

  for (int i = 0 ; i < N_MOTORS ; i++) {
        if (motorForwardLimitSwitchPin[i] != NO_PIN) {
          pinMode(motorForwardLimitSwitchPin[i], INPUT_PULLUP);
          motorForwardLimitSwitchLastRead[i] = isLimitSwitchPressed(motorForwardLimitSwitchPin[i]);
        }
        if (motorBackwardLimitSwitchPin[i] != NO_PIN) {
          pinMode(motorBackwardLimitSwitchPin[i], INPUT_PULLUP);
          motorBackwardLimitSwitchLastRead[i] = isLimitSwitchPressed(motorBackwardLimitSwitchPin[i]);
        }

    pinMode(motorStepPins[i], OUTPUT);
    digitalWrite(motorStepPins[i], LOW);

    pinMode(motorDirPins[i], OUTPUT);
    digitalWrite(motorDirPins[i], LOW);

    setMotorForward(i);
  }
}

bool checkMotorMoveValues(int nPulses, unsigned long stepDelay, int liminaryNPulses, unsigned long liminaryStepDelay) {
  bool error = false;
  if (0 > nPulses || nPulses > 20000) {
    error = true;
  }

  if (200 > stepDelay || stepDelay > 20000) {
    error = true;
  }

  if (liminaryNPulses > 0 && (stepDelay > liminaryStepDelay || liminaryStepDelay > 20000)) {
    error = true;
  }

  if (error) {
    StaticJsonDocument<JSON_OBJECT_SIZE(1)> errorCheckEvent;
    errorCheckEvent[PROTOCOL_CATEGORY] = PROTOCOL_ERROR_CHECK;
    serializeJson(errorCheckEvent, Serial);
    Serial.println();
  }

  return !error;
}

void pulseMotors() {
    currentMicros = micros();

    for (int i = 0 ; i < N_MOTORS ; i++) {
        bool isMotorSupposedToMove = (
            (motorLiminaryNPulses[i] > 0 && motorAccelerationNPulses[i] > 0) ||
            (motorNPulses[i] > 0) ||
            (motorLiminaryNPulses[i] > 0 && motorDecelerationNPulses[i] > 0)
        );
        bool motorForwardLimitSwitchRead = isLimitSwitchPressed(motorForwardLimitSwitchPin[i]);
        bool motorBackwardLimitSwitchRead = isLimitSwitchPressed(motorBackwardLimitSwitchPin[i]);
        bool isDirectionForward = digitalRead(motorDirPins[i]);

        bool hasForwardLimitSwitchJustBeenTriggered = motorForwardLimitSwitchRead && !motorForwardLimitSwitchLastRead[i];
        if (hasForwardLimitSwitchJustBeenTriggered || (isMotorSupposedToMove && isDirectionForward && motorForwardLimitSwitchRead)) {
            sendLimitReachedEvent(i, PROTOCOL_LIMIT_DIRECTION_FORWARD, motorAccelerationNPulses[i] + motorNPulses[i] + motorDecelerationNPulses[i]);
        }

        bool hasBackwardLimitSwitchJustBeenTriggered = motorBackwardLimitSwitchRead && !motorBackwardLimitSwitchLastRead[i];
        if (hasBackwardLimitSwitchJustBeenTriggered || (isMotorSupposedToMove && !isDirectionForward && motorBackwardLimitSwitchRead)) {
            sendLimitReachedEvent(i, PROTOCOL_LIMIT_DIRECTION_BACKWARD, motorAccelerationNPulses[i] + motorNPulses[i] + motorDecelerationNPulses[i]);
        }

        if ((motorForwardLimitSwitchRead && isDirectionForward) || (motorBackwardLimitSwitchRead && !isDirectionForward)) {
            motorNPulses[i] = 0;
            motorAccelerationNPulses[i] = 0;
            motorDecelerationNPulses[i] = 0;
        }

        bool hasForwardLimitSwitchJustBeenReleased = !motorForwardLimitSwitchRead && motorForwardLimitSwitchLastRead[i];
        if (hasForwardLimitSwitchJustBeenReleased) {
            sendLimitReleasedEvent(i, PROTOCOL_LIMIT_DIRECTION_FORWARD, motorAccelerationNPulses[i] + motorNPulses[i] + motorDecelerationNPulses[i]);
        }

        bool hasBackwardLimitSwitchJustBeenReleased = !motorBackwardLimitSwitchRead && motorBackwardLimitSwitchLastRead[i];
        if (hasBackwardLimitSwitchJustBeenReleased) {
            sendLimitReleasedEvent(i, PROTOCOL_LIMIT_DIRECTION_BACKWARD, motorAccelerationNPulses[i] + motorNPulses[i] + motorDecelerationNPulses[i]);
        }

        if (isMotorSupposedToMove) {
            if (digitalRead(motorStepPins[i])) {
                if (currentMicros - motorPreviousMicros[i] >= 200) {
                    digitalWrite(motorStepPins[i], LOW);
                    motorPreviousMicros[i] = currentMicros;

                    if (motorLiminaryNPulses[i] > 0 && motorAccelerationNPulses[i] > 0) {
                      motorAccelerationNPulses[i]--;
                      if (motorAccelerationNPulses[i] == 0) {
                        motorCurrentStepDelays[i] = motorStepDelays[i];
                      } else {
                        motorCurrentStepDelays[i] =
                          (motorLiminaryStepDelays[i] - motorStepDelays[i]) *
                          ((float) motorAccelerationNPulses[i] / (float) motorLiminaryNPulses[i]) +
                          motorStepDelays[i];
                      }
                    } else if (motorNPulses[i] > 0) {
                      motorNPulses[i]--;
                      if (motorNPulses[i] == 0 && motorLiminaryNPulses[i] == 0) {
                        sendMoveCompletedEvent(i);
                      }
                    } else {
                      // motorLiminaryNPulses[i] > 0 && motorDecelerationNPulses[i] > 0
                      // This is guaranteed by the big if above
                      motorDecelerationNPulses[i]--;
                      if (motorDecelerationNPulses[i] == 0) {
                        sendMoveCompletedEvent(i);
                      } else {
                        motorCurrentStepDelays[i] =
                          (motorLiminaryStepDelays[i] - motorStepDelays[i]) *
                          (1 - ((float) motorDecelerationNPulses[i] / (float) motorLiminaryNPulses[i])) +
                          motorStepDelays[i];
                      }
                    }
                }
            } else {
                if (currentMicros - motorPreviousMicros[i] >= motorCurrentStepDelays[i] - 200) {
                    digitalWrite(motorStepPins[i], HIGH);
                    motorPreviousMicros[i] = currentMicros;
                }
            }
        }

        motorForwardLimitSwitchLastRead[i] = motorForwardLimitSwitchRead;
        motorBackwardLimitSwitchLastRead[i] = motorBackwardLimitSwitchRead;
    }
}

void onEvent() {
  DeserializationError error = deserializeJson(receivedDocument, receivedEvent);
  if (error != DeserializationError::Ok) {
    StaticJsonDocument<JSON_OBJECT_SIZE(2)> errorEvent;

    errorEvent[PROTOCOL_CATEGORY] = PROTOCOL_ERROR;
    errorEvent[PROTOCOL_ERROR] = error.c_str();

    serializeJson(errorEvent, RPI_SERIAL);
    RPI_SERIAL.println();
  } else {
    String to = receivedDocument[PROTOCOL_TO];

    if (to == "dxl_radius_wrist") {
      serializeJson(receivedDocument, DYNAMIXEL_RADIUS_WRIST_SERIAL);
      DYNAMIXEL_RADIUS_WRIST_SERIAL.println();
    } else if (to == "dxl_thumb") {
      serializeJson(receivedDocument, DYNAMIXEL_THUMB_SERIAL);
      DYNAMIXEL_THUMB_SERIAL.println();
    } else {
      String category = receivedDocument[PROTOCOL_CATEGORY];

      if (category == PROTOCOL_FORWARD) {
        int motorIndex = receivedDocument[PROTOCOL_MOTOR_INDEX];
        int nPulses = receivedDocument[PROTOCOL_N_PULSES];
        unsigned long stepDelay = receivedDocument[PROTOCOL_STEP_DELAY];
        int liminaryNPulses = receivedDocument[PROTOCOL_LIMINARY_N_PULSES];
        unsigned long liminaryStepDelay = receivedDocument[PROTOCOL_LIMINARY_STEP_DELAY];
        if (!checkMotorMoveValues(nPulses, stepDelay, liminaryNPulses, liminaryStepDelay)) {
          return;
        }
        motorNPulses[motorIndex] = nPulses;
        motorStepDelays[motorIndex] = stepDelay;
        motorLiminaryNPulses[motorIndex] = liminaryNPulses;
        motorAccelerationNPulses[motorIndex] = liminaryNPulses;
        motorDecelerationNPulses[motorIndex] = liminaryNPulses;
        motorLiminaryStepDelays[motorIndex] = liminaryStepDelay;
        if (motorLiminaryNPulses[motorIndex]) {
          motorCurrentStepDelays[motorIndex] = motorLiminaryStepDelays[motorIndex];
        } else {
          motorCurrentStepDelays[motorIndex] = motorStepDelays[motorIndex];
        }
        setMotorForward(motorIndex);
      } else if (category == PROTOCOL_BACKWARD) {
        int motorIndex = receivedDocument[PROTOCOL_MOTOR_INDEX];
        int nPulses = receivedDocument[PROTOCOL_N_PULSES];
        unsigned long stepDelay = receivedDocument[PROTOCOL_STEP_DELAY];
        int liminaryNPulses = receivedDocument[PROTOCOL_LIMINARY_N_PULSES];
        unsigned long liminaryStepDelay = receivedDocument[PROTOCOL_LIMINARY_STEP_DELAY];
        if (!checkMotorMoveValues(nPulses, stepDelay, liminaryNPulses, liminaryStepDelay)) {
          return;
        }
        motorNPulses[motorIndex] = nPulses;
        motorStepDelays[motorIndex] = stepDelay;
        motorLiminaryNPulses[motorIndex] = liminaryNPulses;
        motorAccelerationNPulses[motorIndex] = liminaryNPulses;
        motorDecelerationNPulses[motorIndex] = liminaryNPulses;
        motorLiminaryStepDelays[motorIndex] = liminaryStepDelay;
        if (motorLiminaryNPulses[motorIndex]) {
          motorCurrentStepDelays[motorIndex] = motorLiminaryStepDelays[motorIndex];
        } else {
          motorCurrentStepDelays[motorIndex] = motorStepDelays[motorIndex];
        }
        setMotorBackward(motorIndex);
      } else if (category == PROTOCOL_GET_SWITCHES_INFO) {
        StaticJsonDocument<JSON_OBJECT_SIZE(3 + 2 * N_MOTORS)> getSwitchesInfoEvent;
        getSwitchesInfoEvent[PROTOCOL_CATEGORY] = PROTOCOL_GET_SWITCHES_INFO;
        JsonArray forwardSwitches = getSwitchesInfoEvent.createNestedArray(PROTOCOL_LIMIT_DIRECTION_FORWARD);
        JsonArray backwardSwitches = getSwitchesInfoEvent.createNestedArray(PROTOCOL_LIMIT_DIRECTION_BACKWARD);

        for (int i = 0 ; i < N_MOTORS ; i++) {
          forwardSwitches.add(isLimitSwitchPressed(motorForwardLimitSwitchPin[i]));
          backwardSwitches.add(isLimitSwitchPressed(motorBackwardLimitSwitchPin[i]));
        }

        serializeJson(getSwitchesInfoEvent, Serial);
        Serial.println();
      } else if (category == PROTOCOL_STOP) {
        int motorIndex = receivedDocument[PROTOCOL_MOTOR_INDEX];
        motorNPulses[motorIndex] = 0;
        motorAccelerationNPulses[motorIndex] = 0;
        motorDecelerationNPulses[motorIndex] = 0;
      } else if (category == PROTOCOL_ELECTROMAGNET) {
        bool magnetize = receivedDocument[PROTOCOL_MAGNETIZE];
        if (magnetize) {
          digitalWrite(ELECTROMAGNET_PIN, HIGH);
        } else {
          digitalWrite(ELECTROMAGNET_PIN, LOW);
        }
      }
    }
  }
}

void onDynamixelRadiusWristEvent() {
  DeserializationError error = deserializeJson(receivedDocument, dynamixelRadiusWristReceivedEvent);
  if (error != DeserializationError::Ok) {
    StaticJsonDocument<JSON_OBJECT_SIZE(3)> errorEvent;

    errorEvent[PROTOCOL_CATEGORY] = PROTOCOL_ERROR;
    errorEvent[PROTOCOL_ERROR] = error.c_str();
    errorEvent[PROTOCOL_FROM] = "dxl_radius_wrist";

    serializeJson(errorEvent, RPI_SERIAL);
    RPI_SERIAL.println();
  } else {
    receivedDocument[PROTOCOL_FROM] = "dxl_radius_wrist";
    serializeJson(receivedDocument, RPI_SERIAL);
    RPI_SERIAL.println();
  }
}

void onDynamixelThumbEvent() {
  DeserializationError error = deserializeJson(receivedDocument, dynamixelThumbReceivedEvent);
  if (error != DeserializationError::Ok) {
    StaticJsonDocument<JSON_OBJECT_SIZE(3)> errorEvent;

    errorEvent[PROTOCOL_CATEGORY] = PROTOCOL_ERROR;
    errorEvent[PROTOCOL_ERROR] = error.c_str();
    errorEvent[PROTOCOL_FROM] = "dxl_thumb";

    serializeJson(errorEvent, RPI_SERIAL);
    RPI_SERIAL.println();
  } else {
    receivedDocument[PROTOCOL_FROM] = "dxl_thumb";
    serializeJson(receivedDocument, RPI_SERIAL);
    RPI_SERIAL.println();
  }
}

void loop() {
  pulseMotors();

  while (RPI_SERIAL.available()) {
    char inChar = (char)
    RPI_SERIAL.read();

    if (inChar == '\n') {
      onEvent();
      receivedEvent = "";
    } else {
      receivedEvent += inChar;
    }
  }

  while (DYNAMIXEL_RADIUS_WRIST_SERIAL.available()) {
    char inChar = (char)
    DYNAMIXEL_RADIUS_WRIST_SERIAL.read();

    if (inChar == '\n') {
      onDynamixelRadiusWristEvent();
      dynamixelRadiusWristReceivedEvent = "";
    } else {
      dynamixelRadiusWristReceivedEvent += inChar;
    }
  }

  while (DYNAMIXEL_THUMB_SERIAL.available()) {
    char inChar = (char)
    DYNAMIXEL_THUMB_SERIAL.read();

    if (inChar == '\n') {
      onDynamixelThumbEvent();
      dynamixelThumbReceivedEvent = "";
    } else {
      dynamixelThumbReceivedEvent += inChar;
    }
  }
}