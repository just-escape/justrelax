#include <SPI.h>
#include <MFRC522.h>
#include <deprecated.h>
#include <require_cpp11.h>
#include <MFRC522Extended.h>

#include <ArduinoJson.h>
#include <FastLED.h>

int rstPins[5] = {5, 6, 7, 8, 9};
#define SS_PIN      10
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

#define STRIP_0_PIN  3
#define STRIP_1_PIN  4
#define STRIP_2_PIN  5
#define MAX_LEDS    23
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB ledStrips[3][MAX_LEDS];

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

void setup() {
  Serial.begin(9600);

  SPI.begin();

  analogWrite(5, LOW);
  analogWrite(6, LOW);
  analogWrite(7, LOW);
  analogWrite(9, LOW);

  FastLED.addLeds<LED_TYPE, STRIP_0_PIN, COLOR_ORDER>(ledStrips[0], MAX_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, STRIP_1_PIN, COLOR_ORDER>(ledStrips[1], MAX_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, STRIP_2_PIN, COLOR_ORDER>(ledStrips[2], MAX_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
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

  event["event_type"] = "rfid_read";
  event["reader"] = currentReaderIndex;
  JsonArray value = event.createNestedArray("value");
  for (int i = 0 ; i < readers[currentReaderIndex].uid.size ; i++) {
    value.add(readers[currentReaderIndex].uid.uidByte[i]);
  }

  serializeJson(event, Serial);
  Serial.println();
}

void pushCurrentReaderNullValue() {
  StaticJsonDocument<JSON_OBJECT_SIZE(3)> event;

  event["event_type"] = "rfid_read";
  event["reader"] = currentReaderIndex;
  event["value"] = (char *)NULL;

  serializeJson(event, Serial);
  Serial.println();
}

void loop() {
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

  analogWrite(rstPins[currentReaderIndex], LOW);
  currentReaderIndex = (currentReaderIndex + 1) % 5;
}

void onEvent() {
  DeserializationError error = deserializeJson(receivedDocument, receivedEvent);
  if (error != DeserializationError::Ok) {
    Serial.println(error.c_str());
  } else {
    String eventType = receivedDocument["event_type"];

    if (eventType == "led") {
      int strip = receivedDocument["strip"];
      int led = receivedDocument["led"];
      int r = receivedDocument["r"];
      int g = receivedDocument["g"];
      int b = receivedDocument["b"];

      ledStrips[strip][led].r = r;
      ledStrips[strip][led].g = g;
      ledStrips[strip][led].b = b;

      if (receivedDocument.containsKey("commit")) {
        boolean commit = receivedDocument["commit"];
        if (commit) {
          FastLED.show();
        }
      } else {
        // By default
        FastLED.show();
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
