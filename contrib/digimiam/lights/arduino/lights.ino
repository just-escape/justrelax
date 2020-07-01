#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_ON "n"
#define PROTOCOL_OFF "f"
#define PROTOCOL_CHANNELS "h"
#define PROTOCOL_SET_COLOR "s"
#define PROTOCOL_COLOR "r"
#define PROTOCOL_FADE_BRIGHTNESS "b"
#define PROTOCOL_TARGET_BRIGHTNESS "t"

#define CHANNELS 10

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

unsigned long currentTime;
unsigned long deltaTime;
unsigned long deltaTimeModulus1000;
unsigned long lastCycleStart;

int pins[CHANNELS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
int colors[CHANNELS] = {0};
int colorsTimesBrightnesses[CHANNELS] = {0};
int brightnesses[CHANNELS] = {0};
int targetBrightnesses[CHANNELS] = {0};
bool isOn[CHANNELS] = {false};
bool isHigh[CHANNELS] = {false};

int cyclesCounter = 0;

void setup() {
  for (int i = 0 ; i < CHANNELS ; i++) {
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], LOW);
  }

  lastCycleStart = micros();
  Serial.begin(9600);
}

void loop() {
  currentTime = micros();
  deltaTime = currentTime - lastCycleStart;

  if (deltaTime > 1000) {
    lastCycleStart = currentTime;
    cyclesCounter++;

    for (int i = 0 ; i < CHANNELS ; i++) {
      isHigh[i] = true && isOn[i];
    }

    if (cyclesCounter % 5 == 0) {
      for (int i = 0 ; i < CHANNELS ; i++) {
        if (targetBrightnesses[i] > brightnesses[i]) {
          brightnesses[i]++;
          colorsTimesBrightnesses[i] = colors[i] * brightnesses[i];
        } else if (targetBrightnesses[i] < brightnesses[i]) {
          brightnesses[i]--;
          colorsTimesBrightnesses[i] = colors[i] * brightnesses[i];
        }
      }
    }
  }

  deltaTimeModulus1000 = deltaTime % 1000;

  for (int i = 0 ; i < CHANNELS ; i++) {
    if (deltaTimeModulus1000 > colorsTimesBrightnesses[i]) {
      isHigh[i] = false;
    }

    digitalWrite(pins[i], isHigh[i]);
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

    if (category == PROTOCOL_ON) {
      for (int i = 0 ; i < CHANNELS ; i++) {
        if ((channelsBitmask & currentChannelBit) == currentChannelBit) {
          isOn[i] = true;
        }
        currentChannelBit = currentChannelBit << 1;
      }
    } else if (category == PROTOCOL_OFF) {
      for (int i = 0 ; i < CHANNELS ; i++) {
        if ((channelsBitmask & currentChannelBit) == currentChannelBit) {
          isOn[i] = false;
        }
        currentChannelBit = currentChannelBit << 1;
      }
    } else if (category == PROTOCOL_FADE_BRIGHTNESS) {
      int targetBrightness = receivedDocument[PROTOCOL_TARGET_BRIGHTNESS];
      for (int i = 0 ; i < CHANNELS ; i++) {
        if ((channelsBitmask & currentChannelBit) == currentChannelBit) {
          targetBrightnesses[i] = targetBrightness;
        }
        currentChannelBit = currentChannelBit << 1;
      }
    } else if (category == PROTOCOL_SET_COLOR) {
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
