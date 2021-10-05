#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"
#define PROTOCOL_ERROR_CHECK "ec"

#define PROTOCOL_FROM "fr"
#define PROTOCOL_TO "to"

#define PROTOCOL_HOMING "h"
#define PROTOCOL_FORWARD "f"
#define PROTOCOL_BACKWARD "b"
#define PROTOCOL_STEP_DELAY "sd"
#define PROTOCOL_MOTOR_INDEX "i"
#define PROTOCOL_N_PULSES "n"
#define PROTOCOL_LIMINARY_STEP_DELAY "lsd"
#define PROTOCOL_LIMINARY_N_PULSES "ln"
#define PROTOCOL_STOP "stop"

#define PROTOCOL_NO_HOMING "nh"
#define PROTOCOL_HOMING_COMPLETE "hc"
#define PROTOCOL_HOMING_REMAINING_STEPS "hrs"
#define PROTOCOL_HOMING_FAILED "hf"

#define PROTOCOL_ELECTROMAGNET "e"
#define PROTOCOL_MAGNETIZE "m"

#define RPI_SERIAL Serial
#define DYNAMIXEL_SERIAL Serial2

String receivedEvent = "";
String dynamixelReceivedEvent = "";
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
bool isMotorInHomingMode[N_MOTORS] = {false, false, false};
#define NO_LIMIT_SWITCH_PIN -1
int motorLimitSwitchPin[N_MOTORS] = {24, 26, 28};
bool motorIsHomingDirectionForward[N_MOTORS] = {false, true, true};

#define ELECTROMAGNET_PIN 52

void setMotorForward(int motorIndex) {
  digitalWrite(motorDirPins[motorIndex], HIGH);
}

void setMotorBackward(int motorIndex) {
  digitalWrite(motorDirPins[motorIndex], LOW);
}

void sendHomingFailedEvent(int motorIndex) {
    StaticJsonDocument<JSON_OBJECT_SIZE(2)> homingFailedEvent;
    homingFailedEvent[PROTOCOL_CATEGORY] = PROTOCOL_HOMING_FAILED;
    homingFailedEvent[PROTOCOL_MOTOR_INDEX] = motorIndex;
    serializeJson(homingFailedEvent, Serial);
    Serial.println();
}

void setup() {
  RPI_SERIAL.begin(9600);
  DYNAMIXEL_SERIAL.begin(9600);

  pinMode(ELECTROMAGNET_PIN, OUTPUT);
  digitalWrite(ELECTROMAGNET_PIN, LOW);

  for (int i = 0 ; i < N_MOTORS ; i++) {
    if (motorLimitSwitchPin[i] != NO_LIMIT_SWITCH_PIN) {
      pinMode(motorLimitSwitchPin[i], INPUT_PULLUP);
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
        if (motorIsHomingDirectionForward[i] == digitalRead(motorDirPins[i])) {
          // This is an INPUT_PULLUP pin, so 0 means the switch is triggered
          if (!digitalRead(motorLimitSwitchPin[i])) {
            if (isMotorInHomingMode[i]) {
              StaticJsonDocument<JSON_OBJECT_SIZE(3)> homingCompleteEvent;
              homingCompleteEvent[PROTOCOL_CATEGORY] = PROTOCOL_HOMING_COMPLETE;
              homingCompleteEvent[PROTOCOL_MOTOR_INDEX] = i;
              homingCompleteEvent[PROTOCOL_HOMING_REMAINING_STEPS] = motorNPulses[i];
              serializeJson(homingCompleteEvent, Serial);
              Serial.println();
              isMotorInHomingMode[i] = false;
            }
            motorNPulses[i] = 0;
          }
        }

        if (
            (motorLiminaryNPulses[i] > 0 && motorAccelerationNPulses[i] > 0) ||
            (motorNPulses[i] > 0) ||
            (motorLiminaryNPulses[i] > 0 && motorDecelerationNPulses[i] > 0)
        ) {
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
                      if (motorNPulses[i] == 0 && motorLiminaryNPulses[i] == 0 && isMotorInHomingMode[i]) {
                        sendHomingFailedEvent(i);
                        isMotorInHomingMode[i] = false;
                      }
                    } else {
                      // motorLiminaryNPulses[i] > 0 && motorDecelerationNPulses[i] > 0
                      // This is guaranteed by the big if above
                      motorDecelerationNPulses[i]--;
                      if (motorDecelerationNPulses[i] == 0) {
                        if (isMotorInHomingMode[i]) {
                          sendHomingFailedEvent(i);
                          isMotorInHomingMode[i] = false;
                        }
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

    if (to == "dxl") {
      serializeJson(receivedDocument, DYNAMIXEL_SERIAL);
      DYNAMIXEL_SERIAL.println();
    } else {
      String category = receivedDocument[PROTOCOL_CATEGORY];

      if (category == PROTOCOL_HOMING) {
        int motorIndex = receivedDocument[PROTOCOL_MOTOR_INDEX];
        if (motorLimitSwitchPin[motorIndex] == NO_LIMIT_SWITCH_PIN) {
          StaticJsonDocument<JSON_OBJECT_SIZE(2)> noHomingEvent;
          noHomingEvent[PROTOCOL_CATEGORY] = PROTOCOL_NO_HOMING;
          noHomingEvent[PROTOCOL_MOTOR_INDEX] = motorIndex;
          serializeJson(noHomingEvent, Serial);
          Serial.println();
          return;
        }
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
        if (motorIsHomingDirectionForward[motorIndex]) {
          setMotorForward(motorIndex);
        } else {
          setMotorBackward(motorIndex);
        }
        isMotorInHomingMode[motorIndex] = true;
      } else if (category == PROTOCOL_FORWARD) {
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
        isMotorInHomingMode[motorIndex] = false;
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
        isMotorInHomingMode[motorIndex] = false;
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

void onDynamixelEvent() {
  DeserializationError error = deserializeJson(receivedDocument, dynamixelReceivedEvent);
  if (error != DeserializationError::Ok) {
    StaticJsonDocument<JSON_OBJECT_SIZE(2)> errorEvent;

    errorEvent[PROTOCOL_CATEGORY] = PROTOCOL_ERROR;
    errorEvent[PROTOCOL_ERROR] = error.c_str();

    serializeJson(errorEvent, RPI_SERIAL);
    RPI_SERIAL.println();
  } else {
    receivedDocument[PROTOCOL_FROM] = "dxl";
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

  while (DYNAMIXEL_SERIAL.available()) {
    char inChar = (char)
    DYNAMIXEL_SERIAL.read();

    if (inChar == '\n') {
      onDynamixelEvent();
      dynamixelReceivedEvent = "";
    } else {
      dynamixelReceivedEvent += inChar;
    }
  }
}