#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_SET_COLOR "s"
#define PROTOCOL_CHANNELS "h"
#define PROTOCOL_COLOR "r"

#define CHANNELS 10

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

unsigned long currentTime;
unsigned long deltaTime;
unsigned long deltaTimeModulus1000;
unsigned long lastCycleStart;

// White, Purple, Red, Green, Blue's red, Blue's green, Blue's blue, Orange's red, Orange's green, Orange's blue
int lightPins[CHANNELS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
float colors[CHANNELS] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
byte isOnPins[CHANNELS] = {48, 52, 46, 50, 42, 42, 42, 44, 44, 44};
bool isHigh[CHANNELS] = {false};

void setup() {
  for (int i = 0 ; i < CHANNELS ; i++) {
    pinMode(lightPins[i], OUTPUT);
    pinMode(isOnPins[i], INPUT);
  }

  lastCycleStart = micros();
  Serial.begin(9600);
}

void loop() {
  currentTime = micros();
  deltaTime = currentTime - lastCycleStart;

  if (deltaTime > 1000) {
    lastCycleStart = currentTime;

    for (int i = 0 ; i < CHANNELS ; i++) {
      isHigh[i] = digitalRead(isOnPins[i]);
    }
  }

  deltaTimeModulus1000 = deltaTime % 1000;

  for (int i = 0 ; i < CHANNELS ; i++) {
    if (deltaTimeModulus1000 > colors[i]) {
      isHigh[i] = false;
    }

    digitalWrite(lightPins[i], isHigh[i]);
  }
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
          colors[i] = color;
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
