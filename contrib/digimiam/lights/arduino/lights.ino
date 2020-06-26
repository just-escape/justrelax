#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_ON "n"
#define PROTOCOL_OFF "f"
#define PROTOCOL_CHANNEL "h"
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
int highRatios[CHANNELS] = {0};
int targetHighRatios[CHANNELS] = {0};
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
        if (targetHighRatios[i] > highRatios[i]) {
          highRatios[i]++;
        } else if (targetHighRatios[i] < highRatios[i]) {
          highRatios[i]--;
        }
      }
    }
  }

  deltaTimeModulus1000 = deltaTime % 1000;

  for (int i = 0 ; i < CHANNELS ; i++) {
    if (deltaTimeModulus1000 > highRatios[i]) {
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
    int channel = receivedDocument[PROTOCOL_CHANNEL];

    if (category == PROTOCOL_ON) {
      isOn[channel] = true;
    } else if (category == PROTOCOL_OFF) {
      isOn[channel] = false;
    } else if (category == PROTOCOL_FADE_BRIGHTNESS) {
      int targetBrightness = receivedDocument[PROTOCOL_TARGET_BRIGHTNESS];
      targetHighRatios[channel] = targetBrightness;
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
