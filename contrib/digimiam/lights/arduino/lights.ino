#include <ArduinoJson.h>
#include <Gaussian.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_SET_COLOR "s"
#define PROTOCOL_CHANNELS "h"
#define PROTOCOL_COLOR "r"
#define PROTOCOL_STOP_GLITCH_ANIMATION "sga"
#define PROTOCOL_ANIMATE_GLITCH "g"
#define PROTOCOL_ANIMATION_SHORT_GLITCH_PM "sg"
#define PROTOCOL_ANIMATION_SHORT_DIMMED_GLITCH_PM "sdg"
#define PROTOCOL_ANIMATION_LONG_GLITCH_PM "lg"
#define PROTOCOL_ANIMATION_LONG_DIMMED_GLITCH_PM "ldg"
#define PROTOCOL_ANIMATION_STABILITY "st"
#define PROTOCOL_ANIMATION_STABILITY_DURATION "std"

#define CHANNELS 10

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

// White, Purple, Red, Green, Blue's red, Blue's green, Blue's blue, Orange's red, Orange's green, Orange's blue
int lightPins[CHANNELS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
float colorConfiguredFrequencies[CHANNELS] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
float colorAnimatedFrequencies[CHANNELS] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
float colorCycles[CHANNELS] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
byte isOnPins[CHANNELS] = {48, 52, 46, 50, 42, 42, 42, 44, 44, 44};
bool isHigh[CHANNELS] = {false};

bool isColorGlitched[CHANNELS] = {false};

unsigned long currentMillis;
unsigned long lastMillis[CHANNELS] = {0};
unsigned long waitUntilNextTransition[CHANNELS] = {100};
long randNumber;
double tmpGaussian;
Gaussian colorNoise(0, 12);
Gaussian longGlitchGaussian(500, 200);
Gaussian shortGlitchGaussian(0, 10);

int animationShortGlitchPerMille[CHANNELS] = {36};
int animationShortDimmedGlitchPerMille[CHANNELS] = {36};
int animationLongGlitchPerMille[CHANNELS] = {39};
int animationLongDimmedGlitchPerMille[CHANNELS] = {40};
int animationStabilityPerMille[CHANNELS] = {45};
int animationStabilityDuration[CHANNELS] = {15000};

void setup() {
  for (int i = 0 ; i < CHANNELS ; i++) {
    pinMode(lightPins[i], OUTPUT);
    pinMode(isOnPins[i], INPUT);
    isColorGlitched[i] = false;
  }

  Serial.begin(9600);
}

void animateNone(int colorIndex) {
  colorAnimatedFrequencies[colorIndex] = colorConfiguredFrequencies[colorIndex];
  waitUntilNextTransition[colorIndex] = 100;
}

void animateGlitch(int colorIndex) {
  randNumber = random(1, 1000);
  if (randNumber <= animationShortGlitchPerMille[colorIndex]) {
    // Short glitch
    colorAnimatedFrequencies[colorIndex] = 0;
    tmpGaussian = shortGlitchGaussian.random();
    waitUntilNextTransition[colorIndex] = max(min((int) tmpGaussian, 30), 0);
  } else if (randNumber <= animationShortDimmedGlitchPerMille[colorIndex]) {
    // Short glitch with a dim color
    colorAnimatedFrequencies[colorIndex] = 0.05 * colorConfiguredFrequencies[colorIndex];
    tmpGaussian = shortGlitchGaussian.random();
    waitUntilNextTransition[colorIndex] = max(min((int) tmpGaussian, 30), 0);
  } else if (randNumber <= animationLongGlitchPerMille[colorIndex]) {
    // Long glitch
    colorAnimatedFrequencies[colorIndex] = 0;
    tmpGaussian = longGlitchGaussian.random();
    waitUntilNextTransition[colorIndex] = max(min((int) tmpGaussian, 800), 200);
  } else if (randNumber <= animationLongDimmedGlitchPerMille[colorIndex]) {
    // Long glitch with a dim color
    colorAnimatedFrequencies[colorIndex] = 0.05 * colorConfiguredFrequencies[colorIndex];
    tmpGaussian = longGlitchGaussian.random();
    waitUntilNextTransition[colorIndex] = max(min((int) tmpGaussian, 800), 200);
  } else if (randNumber <= animationStabilityPerMille[colorIndex]) {
    // Normal color for a long time
    colorAnimatedFrequencies[colorIndex] = colorConfiguredFrequencies[colorIndex];
    waitUntilNextTransition[colorIndex] = animationStabilityDuration[colorIndex];
  } else {
    // Normal color
    colorAnimatedFrequencies[colorIndex] = colorConfiguredFrequencies[colorIndex];
    waitUntilNextTransition[colorIndex] = 10;
  }
}

void animateColorFrequencies() {
  currentMillis = millis();
  for (int i = 0 ; i < CHANNELS ; i++) {
    if (currentMillis - lastMillis[i] >= waitUntilNextTransition[i]) {
      if (isColorGlitched[i]) {
        animateGlitch(i);
      } else {
        animateNone(i);
      }
      lastMillis[i] = currentMillis;
    }
  }
}

void PWMCycles() {
  for (int i = 0 ; i < CHANNELS ; i++) {
    if (digitalRead(isOnPins[i])) {
      if (colorAnimatedFrequencies[i] > 0) {
        digitalWrite(lightPins[i], HIGH);
      }
    } else {
      digitalWrite(lightPins[i], LOW);
    }
  }

  for (int cycle = 0 ; cycle < 50 ; cycle++) {
    for (int i = 0 ; i < CHANNELS ; i++) {
      if (cycle >= colorAnimatedFrequencies[i]) {
        digitalWrite(lightPins[i], LOW);
      }
    }
    delayMicroseconds(200);
  }
}

void loop() {
  animateColorFrequencies();
  PWMCycles();
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
    int channelsBitmask = receivedDocument[PROTOCOL_CHANNELS];
    int currentChannelBit = 1;

    if (category == PROTOCOL_SET_COLOR) {
      int color = receivedDocument[PROTOCOL_COLOR];
      for (int i = 0 ; i < CHANNELS ; i++) {
        if ((channelsBitmask & currentChannelBit) == currentChannelBit) {
          colorConfiguredFrequencies[i] = color;
        }
        currentChannelBit = currentChannelBit << 1;
      }
    } else if (category == PROTOCOL_STOP_GLITCH_ANIMATION) {
      for (int i = 0 ; i < CHANNELS ; i++) {
        if ((channelsBitmask & currentChannelBit) == currentChannelBit) {
          isColorGlitched[i] = false;
        }
        currentChannelBit = currentChannelBit << 1;
      }
    } else if (category == PROTOCOL_ANIMATE_GLITCH) {
      for (int i = 0 ; i < CHANNELS ; i++) {
        if ((channelsBitmask & currentChannelBit) == currentChannelBit) {
          isColorGlitched[i] = true;
          animationShortGlitchPerMille[i] = receivedDocument[PROTOCOL_ANIMATION_SHORT_GLITCH_PM];
          animationShortDimmedGlitchPerMille[i] = (int) receivedDocument[PROTOCOL_ANIMATION_SHORT_DIMMED_GLITCH_PM] + animationShortGlitchPerMille[i];
          animationLongGlitchPerMille[i] = (int) receivedDocument[PROTOCOL_ANIMATION_LONG_GLITCH_PM] + animationShortDimmedGlitchPerMille[i];
          animationLongDimmedGlitchPerMille[i] = (int) receivedDocument[PROTOCOL_ANIMATION_LONG_DIMMED_GLITCH_PM] + animationLongGlitchPerMille[i];
          animationStabilityPerMille[i] = (int) receivedDocument[PROTOCOL_ANIMATION_STABILITY] + animationLongDimmedGlitchPerMille[i];
          animationStabilityDuration[i] = receivedDocument[PROTOCOL_ANIMATION_STABILITY_DURATION];
        }
        currentChannelBit = currentChannelBit << 1;
      }
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
