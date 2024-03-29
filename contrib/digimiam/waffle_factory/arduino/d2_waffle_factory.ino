#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#include <FastLED.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"
#define PROTOCOL_ERROR_CHECK "ec"

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

#define PROTOCOL_SET_LED_TARGET_FREQ "t"
#define PROTOCOL_SET_LED_FREQ "q"
#define PROTOCOL_LED_INDEX "i"
#define PROTOCOL_LED_FREQ_VALUE "v"
#define PROTOCOL_LED_FREQ_STEP "s"

#define PROTOCOL_BASKET_LED_ON "kon"
#define PROTOCOL_BASKET_LED_OFF "koff"
#define PROTOCOL_BASKET_LED_BLINK "kblink"

#define PROTOCOL_TURN_OVEN_ON "oon"
#define PROTOCOL_TURN_OVEN_OFF "ooff"

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

unsigned long currentMicros = 0;

#define N_MOTORS 6
const int motorStepPins[N_MOTORS] = {50, 48, 46, 44, 42, 40};
const int motorDirPins[N_MOTORS] = {51, 49, 47, 45, 43, 41};
unsigned long motorLiminaryStepDelays[N_MOTORS] = {1500, 1500, 1500, 1500, 1500, 1500};
unsigned long motorStepDelays[N_MOTORS] = {1500, 1500, 1500, 1500, 1500, 1500};
unsigned long motorCurrentStepDelays[N_MOTORS] = {1500, 1500, 1500, 1500, 1500, 1500};
unsigned long motorPreviousMicros[N_MOTORS] = {0, 0, 0, 0, 0, 0};
int motorLiminaryNPulses[N_MOTORS] = {0, 0, 0, 0, 0, 0};
int motorAccelerationNPulses[N_MOTORS] = {0, 0, 0, 0, 0, 0};
int motorNPulses[N_MOTORS] = {0, 0, 0, 0, 0, 0};
int motorDecelerationNPulses[N_MOTORS] = {0, 0, 0, 0, 0, 0};
#define NO_PIN -1
int motorForwardLimitSwitchPin[N_MOTORS] = {24, 35, 28, 30, NO_PIN, 34};
bool motorForwardLimitSwitchLastRead[N_MOTORS] = {false, false, false, false, false, false};
int motorBackwardLimitSwitchPin[N_MOTORS] = {NO_PIN, 26, 37, NO_PIN, 32, NO_PIN};
bool motorBackwardLimitSwitchLastRead[N_MOTORS] = {false, false, false, false, false, false};

#define N_LED 2
byte ledPins[N_LED] = {2, 3};
float ledPWM[N_LED] = {0, 0};
float ledFreq[N_LED] = {0, 0};
float ledTargetFreq[N_LED] = {0, 0};
float ledTargetFreqStep[N_LED] = {0, 0};
int ledCycle[N_LED] = {0, 0};
unsigned long ledPreviousMicros[N_LED] = {0, 0};

#define N_BASKET_LED 4
#define BASKET_LED_PIN 8
bool basketLedBlinking = false;
bool basketLedBlinkOn = false;
Adafruit_NeoPixel basketLed = Adafruit_NeoPixel(N_BASKET_LED, BASKET_LED_PIN, NEO_GRB + NEO_KHZ800);
unsigned long basketLedPreviousMicros = 0;

#define N_OVEN_LED 22
#define OVEN_LED_PIN 9
CRGBArray<N_OVEN_LED> ovenLed;
bool isOvenTurnedOn = false;
unsigned long ovenLedPreviousMicros = 0;
static byte heat[N_OVEN_LED];
bool gReverseDirection = false;
// There are two main parameters you can play with to control the look and
// feel of your fire: COOLING (used in step 1 above), and SPARKING (used
// in step 3 above).
//
// COOLING: How much does the air cool as it rises?
// Less cooling = taller flames.  More cooling = shorter flames.
// Default 50, suggested range 20-100
#define COOLING  55

// SPARKING: What chance (out of 255) is there that a new spark will be lit?
// Higher chance = more roaring fire.  Lower chance = more flickery fire.
// Default 120, suggested range 50-200.
#define SPARKING 120

void setMotorForward(int motorIndex) {
    digitalWrite(motorDirPins[motorIndex], HIGH);
}

void setMotorBackward(int motorIndex) {
    digitalWrite(motorDirPins[motorIndex], LOW);
}

void resetOvenLed() {
    for (int i = 0 ; i < N_OVEN_LED ; i++) {
        heat[i] = 0;
        ovenLed[i] = CRGB(0, 0, 0);
    }
    FastLED.show();
}

bool isLimitSwitchPressed(int pin) {
    if (pin == NO_PIN) {
        return false;
    }

    // Limit switches are INPUT_PULLUP pins, so 0 means the switch is triggered
    return !digitalRead(pin);
}

void setup() {
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
        motorPreviousMicros[i] = micros();

        setMotorForward(i);
    }

    currentMicros = micros();

    for (int i = 0 ; i < N_LED ; i++) {
        pinMode(ledPins[i], OUTPUT);
    }

    basketLed.begin();

    FastLED.setMaxPowerInVoltsAndMilliamps(5, 4000);
    FastLED.addLeds<WS2811,OVEN_LED_PIN,GRB>(ovenLed, N_OVEN_LED).setCorrection(TypicalLEDStrip);
    resetOvenLed();

    Serial.begin(9600);

    delay(100);
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

void updateMotorClocks() {
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

void blinkBasketLedIfNecessary() {
    if (basketLedBlinking) {
        currentMicros = micros();
        if (currentMicros - basketLedPreviousMicros >= 1000000) {
            basketLedPreviousMicros = currentMicros;
            basketLedBlinkOn = !basketLedBlinkOn;

            for (int i = 0 ; i < N_BASKET_LED - 1 ; i++) {
                if (basketLedBlinkOn) {
                    basketLed.setPixelColor(i, basketLed.Color(0, 255, 0));
                } else {
                    basketLed.setPixelColor(i, basketLed.Color(0, 0, 0));
                }
            }
            if (basketLedBlinkOn) {
                basketLed.setPixelColor(N_BASKET_LED - 1, basketLed.Color(255, 255, 255));
            } else {
                basketLed.setPixelColor(N_BASKET_LED - 1, basketLed.Color(0, 0, 0));
            }
            basketLed.show();
        }
    }
}

// Fire2012 by Mark Kriegsman, July 2012
// as part of "Five Elements" shown here: http://youtu.be/knWiGsmgycY
////
// This basic one-dimensional 'fire' simulation works roughly as follows:
// There's a underlying array of 'heat' cells, that model the temperature
// at each point along the line.  Every cycle through the simulation,
// four steps are performed:
//  1) All cells cool down a little bit, losing heat to the air
//  2) The heat from each cell drifts 'up' and diffuses a little
//  3) Sometimes randomly new 'sparks' of heat are added at the bottom
//  4) The heat from each cell is rendered as a color into the leds array
//     The heat-to-color mapping uses a black-body radiation approximation.
//
// Temperature is in arbitrary units from 0 (cold black) to 255 (white hot).
//
// This simulation scales it self a bit depending on NUM_LEDS; it should look
// "OK" on anywhere from 20 to 100 LEDs without too much tweaking.
//
// I recommend running this simulation at anywhere from 30-100 frames per second,
// meaning an interframe delay of about 10-35 milliseconds.
//
// Looks best on a high-density LED setup (60+ pixels/meter).
void updateOvenLed() {
    if (isOvenTurnedOn) {
        currentMicros = micros();
        // 18 FPS
        if (currentMicros - ovenLedPreviousMicros >= 1000000 / 18) {
            ovenLedPreviousMicros = currentMicros;

            // Step 1.  Cool down every cell a little
            for( int i = 0; i < N_OVEN_LED; i++) {
               heat[i] = qsub8( heat[i],  random8(0, ((COOLING * 10) / N_OVEN_LED) + 2));
            }

            // Step 2.  Heat from each cell drifts 'up' and diffuses a little
            for( int k= N_OVEN_LED - 1; k >= 2; k--) {
              heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2] ) / 3;
            }

            // Step 3.  Randomly ignite new 'sparks' of heat near the bottom
            if( random8() < SPARKING ) {
              int y = random8(7);
              heat[y] = qadd8( heat[y], random8(160,255) );
            }

            // Step 4.  Map from heat cells to LED colors
            for( int j = 0; j < N_OVEN_LED; j++) {
              CRGB color = HeatColor( heat[j]);
              int pixelnumber;
              if( gReverseDirection ) {
                pixelnumber = (N_OVEN_LED-1) - j;
              } else {
                pixelnumber = j;
              }
              ovenLed[pixelnumber] = color;
            }

            FastLED.show();
        }
    }
}

void loop() {
    updateMotorClocks();
    processLEDPWM();
    blinkBasketLedIfNecessary();
    updateOvenLed();
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
    } else if (category == PROTOCOL_BASKET_LED_ON) {
      basketLedBlinking = false;
      for (int i = 0 ; i < N_BASKET_LED - 1 ; i++) {
        basketLed.setPixelColor(i, basketLed.Color(0, 255, 0));
      }
      basketLed.setPixelColor(N_BASKET_LED - 1, basketLed.Color(255, 255, 255));
      basketLed.show();
    } else if (category == PROTOCOL_BASKET_LED_OFF) {
      basketLedBlinking = false;
      for (int i = 0 ; i < N_BASKET_LED ; i++) {
        basketLed.setPixelColor(i, basketLed.Color(0, 0, 0));
      }
      basketLed.show();
    } else if (category == PROTOCOL_BASKET_LED_BLINK) {
      basketLedBlinking = true;
    } else if (category == PROTOCOL_TURN_OVEN_ON) {
      isOvenTurnedOn = true;
    } else if (category == PROTOCOL_TURN_OVEN_OFF) {
      isOvenTurnedOn = false;
      resetOvenLed();
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