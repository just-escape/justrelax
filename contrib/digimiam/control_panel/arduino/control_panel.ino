#include <SPI.h>
#include <MFRC522.h>
#include <deprecated.h>
#include <require_cpp11.h>
#include <MFRC522Extended.h>

#include <ArduinoJson.h>
#include <FastLED.h>

#define PROTOCOL_EVENT_TYPE "e"

#define PROTOCOL_RESET "r"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_MODE_MANUAL "m"

#define PROTOCOL_FLOPPY_READ "f"
#define PROTOCOL_READER "r"
#define PROTOCOL_TAG "t"

#define PROTOCOL_LED_SET_COLOR "s"
#define PROTOCOL_COLORS "c"

int rstPins[5] = {2, 3, 4, 5, 6};
#define SS_PIN      53
MFRC522 readers[5] = {
  MFRC522(SS_PIN, rstPins[0]),
  MFRC522(SS_PIN, rstPins[1]),
  MFRC522(SS_PIN, rstPins[2]),
  MFRC522(SS_PIN, rstPins[3]),
  MFRC522(SS_PIN, rstPins[4])
};
int currentReaderIndex = 0;
byte latestReads[5][10] = {{0}, {0}, {0}, {0}, {0}};
const byte NULL_READ[10] = {0};

#define STATUS_STRIP_PIN  12
#define STATUS_STRIP_LENGTH 3
#define CONTROL_STRIP_PIN  11
#define CONTROL_STRIP_LENGTH 4
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB ledStrips[2][CONTROL_STRIP_LENGTH];  // CONTROL_STRIP_LENGTH as a reference because > STATUS_STRIP_LENGTH

String statusLedsColors = "bbb";
boolean statusLedsBlinkToggle = false;

#define JACK_PIN 43
#define MARMITRON_MODE_PIN 45
#define MANUAL_MODE_PIN 47
boolean manualMode = false;
boolean controlLedsBlinkToggle = false;

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

void setup() {
  Serial.begin(19200);

  SPI.begin();

  for (int i = 0 ; i < 5 ; i++) {
    pinMode(rstPins[i], OUTPUT);
    digitalWrite(rstPins[i], LOW);
  }

  FastLED.addLeds<LED_TYPE, STATUS_STRIP_PIN, COLOR_ORDER>(ledStrips[0], STATUS_STRIP_LENGTH).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, CONTROL_STRIP_PIN, COLOR_ORDER>(ledStrips[1], CONTROL_STRIP_LENGTH).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);

  pinMode(JACK_PIN, OUTPUT);
  digitalWrite(JACK_PIN, HIGH);

  pinMode(MARMITRON_MODE_PIN, INPUT);
  pinMode(MANUAL_MODE_PIN, INPUT);

  delay(100);
}

boolean isValueDifferentFromLatestRead(byte *value) {
  for (int i = 0 ; i < 10 ; i++) {
    if (value[i] != latestReads[currentReaderIndex][i]) {
      return true;
    }
  }

  return false;
}

void saveCurrentReaderValue() {
  for (int i = 0 ; i < 10 ; i++) {
    latestReads[currentReaderIndex][i] = readers[currentReaderIndex].uid.uidByte[i];
  }
}

void resetCurrentReaderValue() {
  for (int i = 0 ; i < 10 ; i++) {
    latestReads[currentReaderIndex][i] = 0;
  }
}

void pushCurrentReaderValue() {
  StaticJsonDocument<JSON_OBJECT_SIZE(3) + JSON_ARRAY_SIZE(10)> event;

  event[PROTOCOL_EVENT_TYPE] = PROTOCOL_FLOPPY_READ;
  event[PROTOCOL_READER] = currentReaderIndex;
  JsonArray value = event.createNestedArray(PROTOCOL_TAG);
  for (int i = 0 ; i < readers[currentReaderIndex].uid.size ; i++) {
    value.add(readers[currentReaderIndex].uid.uidByte[i]);
  }

  serializeJson(event, Serial);
  Serial.println();
}

void pushCurrentReaderNullValue() {
  StaticJsonDocument<JSON_OBJECT_SIZE(3)> event;

  event[PROTOCOL_EVENT_TYPE] = PROTOCOL_FLOPPY_READ;
  event[PROTOCOL_READER] = currentReaderIndex;
  event[PROTOCOL_TAG] = (char *)NULL;

  serializeJson(event, Serial);
  Serial.println();
}

void updateStatusLedsColors() {
  int i;

  statusLedsBlinkToggle = !statusLedsBlinkToggle;

  for (i = 0 ; i <= 2 ; i++) {
    if (statusLedsColors[i] == 'r') {
      ledStrips[0][2 - i].r = 255;
      ledStrips[0][2 - i].g = 0;
      ledStrips[0][2 - i].b = 0;
    } else if (statusLedsColors[i] == 'w') {
      ledStrips[0][2 - i].r = 255;
      ledStrips[0][2 - i].g = 255;
      ledStrips[0][2 - i].b = 255;
    } else if (statusLedsColors[i] == 'g') {
      ledStrips[0][2 - i].r = 0;
      ledStrips[0][2 - i].g = 255;
      ledStrips[0][2 - i].b = 0;
    } else if (statusLedsColors[i] == 'R') {
      if (statusLedsBlinkToggle) {
        ledStrips[0][2 - i].r = 255;
      } else {
        ledStrips[0][2 - i].r = 0;
      }
      ledStrips[0][2 - i].g = 0;
      ledStrips[0][2 - i].b = 0;
    } else if (statusLedsColors[i] == 'G') {
      ledStrips[0][2 - i].r = 0;
      if (statusLedsBlinkToggle) {
        ledStrips[0][2 - i].g = 255;
      } else {
        ledStrips[0][2 - i].g = 0;
      }
      ledStrips[0][2 - i].b = 0;
    } else {
      ledStrips[0][2 - i].r = 0;
      ledStrips[0][2 - i].g = 0;
      ledStrips[0][2 - i].b = 0;
    }
  }
}

void updateControlLedsColors() {
  controlLedsBlinkToggle = !controlLedsBlinkToggle;

  if (digitalRead(MARMITRON_MODE_PIN) == HIGH) {
    if (manualMode) {
      if (controlLedsBlinkToggle) {
        ledStrips[1][3].r = 255;
        ledStrips[1][3].g = 0;
        ledStrips[1][3].b = 0;
      } else {
        ledStrips[1][3].r = 0;
        ledStrips[1][3].g = 0;
        ledStrips[1][3].b = 0;
      }
    } else {
      ledStrips[1][3].r = 0;
      ledStrips[1][3].g = 255;
      ledStrips[1][3].b = 0;
    }
  } else {
    ledStrips[1][3].r = 255;
    ledStrips[1][3].g = 0;
    ledStrips[1][3].b = 0;
  }

  if (digitalRead(MANUAL_MODE_PIN) == HIGH) {
    if (manualMode == false) {
      manualMode = true;

      StaticJsonDocument<JSON_OBJECT_SIZE(2)> manualModeEvent;

      manualModeEvent[PROTOCOL_EVENT_TYPE] = PROTOCOL_MODE_MANUAL;

      serializeJson(manualModeEvent, Serial);
      Serial.println();
    }
    ledStrips[1][1].r = 0;
    ledStrips[1][1].g = 255;
    ledStrips[1][1].b = 0;
  } else {
    if (manualMode) {
      ledStrips[1][1].r = 0;
      ledStrips[1][1].g = 255;
      ledStrips[1][1].b = 0;
    } else {
      ledStrips[1][1].r = 255;
      ledStrips[1][1].g = 0;
      ledStrips[1][1].b = 0;
    }
  }
}

void floppyRead() {
  readers[currentReaderIndex].PCD_Init();

  if (readers[currentReaderIndex].PICC_IsNewCardPresent()) {
    if (readers[currentReaderIndex].PICC_ReadCardSerial()) {
      if (isValueDifferentFromLatestRead(readers[currentReaderIndex].uid.uidByte)) {
        saveCurrentReaderValue();
        pushCurrentReaderValue();
      }
    } else {
      if (isValueDifferentFromLatestRead(NULL_READ)) {
        resetCurrentReaderValue();
        pushCurrentReaderNullValue();
      }
    }
  } else {
    if (isValueDifferentFromLatestRead(NULL_READ)) {
      resetCurrentReaderValue();
      pushCurrentReaderNullValue();
    }
  }

  pinMode(rstPins[currentReaderIndex], OUTPUT);
  digitalWrite(rstPins[currentReaderIndex], LOW);
  currentReaderIndex = (currentReaderIndex + 1) % 5;
  delay(1);
}

void loop() {
  updateStatusLedsColors();
  updateControlLedsColors();
  FastLED.show();

  floppyRead();
}

void onEvent() {
  DeserializationError error = deserializeJson(receivedDocument, receivedEvent);
  if (error != DeserializationError::Ok) {
    StaticJsonDocument<JSON_OBJECT_SIZE(2)> errorEvent;

    errorEvent[PROTOCOL_EVENT_TYPE] = PROTOCOL_ERROR;
    errorEvent[PROTOCOL_ERROR] = error.c_str();

    serializeJson(errorEvent, Serial);
    Serial.println();
  } else {
    String eventType = receivedDocument[PROTOCOL_EVENT_TYPE];

    if (eventType == PROTOCOL_LED_SET_COLOR) {
      String colors = receivedDocument[PROTOCOL_COLORS];
      statusLedsColors = colors;
    } else if (eventType == PROTOCOL_RESET) {
      manualMode = false;
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
