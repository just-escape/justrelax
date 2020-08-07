#include <SPI.h>
#include <MFRC522.h>
#include <deprecated.h>
#include <require_cpp11.h>
#include <MFRC522Extended.h>

#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_READ "r"
#define PROTOCOL_READER_INDEX "i"
#define PROTOCOL_TAG "t"

#define N_READERS 4

int rstPins[N_READERS] = {42, 40, 38, 36};
#define SS_PIN 53
MFRC522 readers[N_READERS];
int currentReaderIndex = 0;
byte latestReads[N_READERS][10];
const byte NULL_READ[10] = {0};

void setup() {
  Serial.begin(19200);

  SPI.begin();

  for (int i = 0 ; i < N_READERS ; i++) {
    readers[i] = MFRC522(SS_PIN, rstPins[i]);
    for (int j = 0 ; j < 10 ; j++) {
      latestReads[i][j] = 0;
    }
    pinMode(rstPins[i], OUTPUT);
    digitalWrite(rstPins[i], LOW);
  }
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

  event[PROTOCOL_CATEGORY] = PROTOCOL_READ;
  event[PROTOCOL_READER_INDEX] = currentReaderIndex;
  JsonArray value = event.createNestedArray(PROTOCOL_TAG);
  for (int i = 0 ; i < readers[currentReaderIndex].uid.size ; i++) {
    value.add(readers[currentReaderIndex].uid.uidByte[i]);
  }

  serializeJson(event, Serial);
  Serial.println();
}

void pushCurrentReaderNullValue() {
  StaticJsonDocument<JSON_OBJECT_SIZE(3)> event;

  event[PROTOCOL_CATEGORY] = PROTOCOL_READ;
  event[PROTOCOL_READER_INDEX] = currentReaderIndex;
  event[PROTOCOL_TAG] = (char *)NULL;

  serializeJson(event, Serial);
  Serial.println();
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
  currentReaderIndex = (currentReaderIndex + 1) % N_READERS;
  delay(1);
}

void loop() {
  floppyRead();
}
