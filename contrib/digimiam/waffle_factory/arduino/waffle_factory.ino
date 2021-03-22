#include <Servo.h>
#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_FORWARD "f"
#define PROTOCOL_BACKWARD "b"
#define PROTOCOL_SET_SPEED "d"
#define PROTOCOL_HIGH_PERIOD "h"
#define PROTOCOL_LOW_PERIOD "l"
#define PROTOCOL_CONVEYOR_INDEX "i"

#define PROTOCOL_MOVE_SERVO "s"
#define PROTOCOL_SERVO_POSITION "p"
#define PROTOCOL_SERVO_INDEX "i"

#define PROTOCOL_SET_LED_TARGET_FREQ "t"
#define PROTOCOL_SET_LED_FREQ "q"
#define PROTOCOL_LED_INDEX "i"
#define PROTOCOL_LED_FREQ_VALUE "v"
#define PROTOCOL_LED_FREQ_STEP "s"

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

unsigned long currentMicros = 0;

#define N_CONVEYORS 3
const int conveyorStepPins[N_CONVEYORS] = {50, 48, 46};
const int conveyorDirPins[N_CONVEYORS] = {51, 49, 47};
bool conveyorIsStepHigh[N_CONVEYORS] = {false, false, false};
unsigned long conveyorStepHighMicros[N_CONVEYORS] = {0, 0, 0};
unsigned long conveyorStepLowMicros[N_CONVEYORS] = {0, 0, 0};
unsigned long conveyorPreviousMicros[N_CONVEYORS] = {0, 0, 0};

#define N_SERVOS 3
Servo servos[N_SERVOS];
int servoPins[N_SERVOS] = {40, 38, 36};

#define N_LED 2
byte ledPins[N_LED] = {2, 3};
float ledPWM[N_LED] = {0, 0};
float ledFreq[N_LED] = {0, 0};
float ledTargetFreq[N_LED] = {0, 0};
float ledTargetFreqStep[N_LED] = {0, 0};
int ledCycle[N_LED] = {0, 0};
unsigned long ledPreviousMicros[N_LED] = {0, 0};

void setConveyorForward(int conveyorIndex) {
    digitalWrite(conveyorDirPins[conveyorIndex], HIGH);
}

void setConveyorBackward(int conveyorIndex) {
    digitalWrite(conveyorDirPins[conveyorIndex], LOW);
}

void setConveyorSpeed(int conveyorIndex, unsigned long lowPeriod, unsigned long highPeriod) {
    conveyorStepLowMicros[conveyorIndex] = lowPeriod;
    conveyorStepHighMicros[conveyorIndex] = highPeriod;
}

void setup() {
    for (int i = 0 ; i < N_CONVEYORS ; i++) {
        pinMode(conveyorStepPins[i], OUTPUT);
        pinMode(conveyorDirPins[i], OUTPUT);
        conveyorPreviousMicros[i] = micros();

        setConveyorForward(i);
    }

    currentMicros = micros();

    for (int i = 0 ; i < N_SERVOS ; i++) {
        servos[i].attach(servoPins[i]);
    }

    for (int i = 0 ; i < N_LED ; i++) {
        pinMode(ledPins[i], OUTPUT);
    }

    Serial.begin(9600);

    delay(100);
}

void updateConveyorClocks() {
    currentMicros = micros();

    for (int i = 0 ; i < N_CONVEYORS ; i++) {
        if (conveyorIsStepHigh[i]) {
            if (
                conveyorStepHighMicros[i] > 0 &&
                currentMicros - conveyorPreviousMicros[i] >= conveyorStepHighMicros[i]
            ) {
                digitalWrite(conveyorStepPins[i], LOW);
                conveyorIsStepHigh[i] = false;
                conveyorPreviousMicros[i] = currentMicros;
            }
        } else {
            if (
                conveyorStepLowMicros[i] > 0 &&
                currentMicros - conveyorPreviousMicros[i] >= conveyorStepLowMicros[i]
            ) {
                digitalWrite(conveyorStepPins[i], HIGH);
                conveyorIsStepHigh[i] = true;
                conveyorPreviousMicros[i] = currentMicros;
            }
        }
    }
}

void processLEDPWM() {
    for (int i = 0 ; i < N_LED; i++) {
        currentMicros = micros();

        if (currentMicros - ledPreviousMicros[i] >= 100) {
            if (ledCycle[i] == 0) {
                if (ledFreq[i] > ledTargetFreq[i]) {
                    if (ledTargetFreqStep[i] == 0) {
                        // Just in case a transition that was not planned is triggered
                        ledFreq[i] -= 0.1;
                    } else {
                        ledFreq[i] -= ledTargetFreqStep[i];
                    }
                } else if (ledFreq[i] < ledTargetFreq[i]) {
                    if (ledTargetFreqStep[i] == 0) {
                        // Just in case a transition that was not planned is triggered
                        ledFreq[i] += 0.1;
                    } else {
                        ledFreq[i] += ledTargetFreqStep[i];
                    }
                }

                ledPWM[i] = 0;

                if (ledFreq[i] > 0) {
                    digitalWrite(ledPins[i], HIGH);
                }
            }

            if (ledPWM[i] < ledFreq[i]) {
                ledPWM[i]++;
            } else {
                digitalWrite(ledPins[i], LOW);
            }

            ledCycle[i] = (ledCycle[i] + 1) % 50;
            ledPreviousMicros[i] = currentMicros;
        }
    }
}

void loop() {
    updateConveyorClocks();
    processLEDPWM();
}

void onEvent() {
  DeserializationError error = deserializeJson(receivedDocument, receivedEvent);
  if (error != DeserializationError::Ok) {
    StaticJsonDocument<JSON_OBJECT_SIZE(2)> errorEvent;

    errorEvent[PROTOCOL_CATEGORY] = PROTOCOL_ERROR;
    errorEvent[PROTOCOL_ERROR] = error.c_str();

    serializeJson(errorEvent, Serial);
    Serial.println();
  } else {
    String category = receivedDocument[PROTOCOL_CATEGORY];

    if (category == PROTOCOL_FORWARD) {
      int conveyorIndex = receivedDocument[PROTOCOL_CONVEYOR_INDEX];
      unsigned long lowPeriod = receivedDocument[PROTOCOL_LOW_PERIOD];
      unsigned long highPeriod = receivedDocument[PROTOCOL_HIGH_PERIOD];
      setConveyorForward(conveyorIndex);
      setConveyorSpeed(conveyorIndex, lowPeriod, highPeriod);
    } else if (category == PROTOCOL_BACKWARD) {
      int conveyorIndex = receivedDocument[PROTOCOL_CONVEYOR_INDEX];
      unsigned long lowPeriod = receivedDocument[PROTOCOL_LOW_PERIOD];
      unsigned long highPeriod = receivedDocument[PROTOCOL_HIGH_PERIOD];
      setConveyorBackward(conveyorIndex);
      setConveyorSpeed(conveyorIndex, lowPeriod, highPeriod);
    } else if (category == PROTOCOL_SET_SPEED) {
      int conveyorIndex = receivedDocument[PROTOCOL_CONVEYOR_INDEX];
      unsigned long lowPeriod = receivedDocument[PROTOCOL_LOW_PERIOD];
      unsigned long highPeriod = receivedDocument[PROTOCOL_HIGH_PERIOD];
      setConveyorSpeed(conveyorIndex, lowPeriod, highPeriod);
    } else if (category == PROTOCOL_MOVE_SERVO) {
      int servoIndex = receivedDocument[PROTOCOL_SERVO_INDEX];
      int position = receivedDocument[PROTOCOL_SERVO_POSITION];
      servos[servoIndex].write(position);
    } else if (category == PROTOCOL_SET_LED_TARGET_FREQ) {
      int ledIndex = receivedDocument[PROTOCOL_LED_INDEX];
      float value = receivedDocument[PROTOCOL_LED_FREQ_VALUE];
      float step = receivedDocument[PROTOCOL_LED_FREQ_STEP];
      ledTargetFreq[ledIndex] = value;
      ledTargetFreqStep[ledIndex] = step;
    } else if (category == PROTOCOL_SET_LED_FREQ) {
      int ledIndex = receivedDocument[PROTOCOL_LED_INDEX];
      float value = receivedDocument[PROTOCOL_LED_FREQ_VALUE];
      ledFreq[ledIndex] = value;
      ledTargetFreq[ledIndex] = value;
    }
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)
    Serial.read();

    if (inChar == '\n') {
      onEvent();
      receivedEvent = "";
    } else {
      receivedEvent += inChar;
    }
  }
}