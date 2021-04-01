#include <Servo.h>
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#include <FastLED.h>

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

#define PROTOCOL_BASKET_LED_ON "kon"
#define PROTOCOL_BASKET_LED_OFF "koff"
#define PROTOCOL_BASKET_LED_BLINK "kblink"

#define PROTOCOL_TURN_OVEN_ON "oon"
#define PROTOCOL_TURN_OVEN_OFF "ooff"

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

void resetOvenLed() {
    for (int i = 0 ; i < N_OVEN_LED ; i++) {
        heat[i] = 0;
        ovenLed[i] = CRGB(0, 0, 0);
    }
    FastLED.show();
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

    basketLed.begin();

    FastLED.setMaxPowerInVoltsAndMilliamps(5, 4000);
    FastLED.addLeds<WS2811,OVEN_LED_PIN,GRB>(ovenLed, N_OVEN_LED).setCorrection(TypicalLEDStrip);
    resetOvenLed();

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
    updateConveyorClocks();
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