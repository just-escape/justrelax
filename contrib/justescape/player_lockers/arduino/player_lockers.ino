#include <SPI.h>
#include <MFRC522.h>
#include <deprecated.h>
#include <require_cpp11.h>
#include <MFRC522Extended.h>

#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"
#define PROTOCOL_READ "r"
#define PROTOCOL_TAG "t"
#define PROTOCOL_OPEN_LOCKERS "o"
#define PROTOCOL_LOCKERS_BITMASK "b"

#define N_READERS 4
#define READ_MAX_FREQ 3000

int rstPin = 42;
#define SS_PIN 53
MFRC522 reader = MFRC522(SS_PIN, rstPin);
unsigned long latestReadMillis = 0;
unsigned long currentMillis = 0;
bool waitForNextRead = false;

#define N_LOCKERS 6
#define LOCKERS_OPENING_TIME 100
int lockerPins[N_LOCKERS] = {2, 3, 4, 5, 6, 7};
unsigned long lockerLastOpenedMillis[N_LOCKERS] = {0};

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

void setup() {
  Serial.begin(19200);

  SPI.begin();

  for (int i = 0 ; i < N_LOCKERS ; i++) {
    pinMode(lockerPins[i], OUTPUT);
  }

  reader.PCD_Init();
}

void pushCurrentReaderValue() {
  StaticJsonDocument<JSON_OBJECT_SIZE(3) + JSON_ARRAY_SIZE(10)> event;

  event[PROTOCOL_CATEGORY] = PROTOCOL_READ;
  JsonArray value = event.createNestedArray(PROTOCOL_TAG);
  for (int i = 0 ; i < reader.uid.size ; i++) {
    value.add(reader.uid.uidByte[i]);
  }

  serializeJson(event, Serial);
  Serial.println();
}

void pushCurrentReaderNullValue() {
  StaticJsonDocument<JSON_OBJECT_SIZE(3)> event;

  event[PROTOCOL_CATEGORY] = PROTOCOL_READ;
  event[PROTOCOL_TAG] = (char *)NULL;

  serializeJson(event, Serial);
  Serial.println();
}

void tagRead() {
  if (waitForNextRead) {
    currentMillis = millis();
    if (currentMillis - latestReadMillis < READ_MAX_FREQ) {
      return;
    } else {
      waitForNextRead = false;
    }
  }

  if (reader.PICC_IsNewCardPresent()) {
    if (reader.PICC_ReadCardSerial()) {
      pushCurrentReaderValue();
      waitForNextRead = true;
      latestReadMillis = millis();
    }
  }
}

void checkLockers() {
  currentMillis = millis();
  for (int i = 0 ; i < N_LOCKERS ; i++) {
    if (currentMillis - lockerLastOpenedMillis[i] < LOCKERS_OPENING_TIME) {
      lockerLastOpenedMillis[i] = -1;
      digitalWrite(lockerPins[i], HIGH);
    }
  }
}

void loop() {
  tagRead();
  checkLockers();
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

    if (category == PROTOCOL_OPEN_LOCKERS) {
      JsonVariant uncastBitmask = receivedDocument[PROTOCOL_LOCKERS_BITMASK];
      unsigned int bitmask = uncastBitmask.as<unsigned int>();
      currentMillis = millis();
      unsigned int currentBit = 1;

      for (int i = 0 ; i < N_LOCKERS ; i++) {
        if ((bitmask & currentBit) == currentBit) {
          digitalWrite(lockerPins[i], LOW);
          lockerLastOpenedMillis[i] = currentMillis;
        }
        currentBit = currentBit << 1;
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
