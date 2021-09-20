#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#include <FastLED.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"
#define PROTOCOL_ERROR_CHECK "ec"

#define PROTOCOL_HOMING "h"
#define PROTOCOL_FORWARD "f"
#define PROTOCOL_BACKWARD "b"
#define PROTOCOL_STEP_DELAY "sd"
#define PROTOCOL_MOTOR_INDEX "i"
#define PROTOCOL_N_PULSES "n"
#define PROTOCOL_LIMINARY_STEP_DELAY "lsd"
#define PROTOCOL_LIMINARY_N_PULSES "ln"
#define PROTOCOL_SET_N_PULSES "snp"

#define PROTOCOL_NO_HOMING "nh"
#define PROTOCOL_HOMING_COMPLETE "hc"
#define PROTOCOL_HOMING_REMAINING_STEPS "hrs"
#define PROTOCOL_HOMING_FAILED "hf"

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
bool isMotorInHomingMode[N_MOTORS] = {false, false, false, false, false, false};
#define NO_LIMIT_SWITCH_PIN -1
int motorLimitSwitchPin[N_MOTORS] = {24, 26, 28, 30, 32, 34};
bool motorIsHomingDirectionForward[N_MOTORS] = {true, false, true, true, false, true};

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

void setup() {
    for (int i = 0 ; i < N_MOTORS ; i++) {
        if (motorLimitSwitchPin[i] != NO_LIMIT_SWITCH_PIN) {
          pinMode(motorLimitSwitchPin[i], INPUT_PULLUP);
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

    if (100 > stepDelay || stepDelay > 20000) {
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

void sendHomingFailedEvent(int motorIndex) {
    StaticJsonDocument<JSON_OBJECT_SIZE(2)> homingFailedEvent;
    homingFailedEvent[PROTOCOL_CATEGORY] = PROTOCOL_HOMING_FAILED;
    homingFailedEvent[PROTOCOL_MOTOR_INDEX] = motorIndex;
    serializeJson(homingFailedEvent, Serial);
    Serial.println();
}

void updateMotorClocks() {
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
            return;
          }
        }

        if (
            (motorLiminaryNPulses[i] > 0 && motorAccelerationNPulses[i] > 0) ||
            (motorNPulses[i] > 0) ||
            (motorLiminaryNPulses[i] > 0 && motorDecelerationNPulses[i] > 0)
        ) {
            if (digitalRead(motorStepPins[i])) {
                if (currentMicros - motorPreviousMicros[i] >= 100) {
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
                if (currentMicros - motorPreviousMicros[i] >= motorCurrentStepDelays[i] - 100) {
                    digitalWrite(motorStepPins[i], HIGH);
                    motorPreviousMicros[i] = currentMicros;
                }
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
    } else if (category == PROTOCOL_SET_N_PULSES) {
      int motorIndex = receivedDocument[PROTOCOL_MOTOR_INDEX];
      int nPulses = receivedDocument[PROTOCOL_N_PULSES];
      motorNPulses[motorIndex] = nPulses;
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