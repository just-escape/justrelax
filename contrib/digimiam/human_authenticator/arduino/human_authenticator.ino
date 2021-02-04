#include <ArduinoJson.h>
#include <SoftwareSerial.h>
#include <Adafruit_NeoPixel.h>

#define PROTOCOL_CATEGORY "c"

// Sent events
#define PROTOCOL_ERROR "e"
#define PROTOCOL_AUTHENTICATE "a"
#define PROTOCOL_CANCEL_AUTHENTICATION "c"

// Received events
#define PROTOCOL_STATUS_PLAYING "p"
#define PROTOCOL_STATUS_DISABLED "d"
#define PROTOCOL_STATUS_SUCCESS "w"

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

String status = "disabled";

bool read;
unsigned long currentMillis = 0;

SoftwareSerial rfidReader = SoftwareSerial(10, 11);
unsigned long rfidPreviousMillis = 0;
bool isSomethingBeingSent = false;
#define RFID_TIME_THRESHOLD 2000

#define LED_PIN 7
#define N_LEDS 3
#define LOADING_STEPS 30
#define LOADING_STEPS_DELAY 100
byte ledIndexes[3] = {2, 1, 0};
byte loading = false;
byte loadingStep = 0;
unsigned long loadingStepPreviousMillis = 0;
byte loadingSteps[LOADING_STEPS][3][3] = {
  {{10, 10, 10}, {10, 10, 10}, {10, 10, 10}},
  {{10, 10, 10}, {10, 10, 10}, {10, 10, 10}},
  {{0, 0, 0}, {10, 10, 10}, {10, 10, 10}},
  {{0, 0, 0}, {0, 0, 0}, {10, 10, 10}},
  {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
  {{10, 10, 10}, {0, 0, 0}, {0, 0, 0}},
  {{10, 10, 10}, {10, 10, 10}, {0, 0, 0}},
  {{10, 10, 10}, {10, 10, 10}, {10, 10, 10}},
  {{0, 0, 0}, {10, 10, 10}, {10, 10, 10}},
  {{0, 0, 0}, {0, 0, 0}, {10, 10, 10}},
  {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
  {{10, 10, 10}, {0, 0, 0}, {0, 0, 0}},
  {{10, 10, 10}, {10, 10, 10}, {0, 0, 0}},
  {{10, 10, 10}, {10, 10, 10}, {10, 10, 10}},
  {{0, 0, 0}, {10, 10, 10}, {10, 10, 10}},
  {{0, 0, 0}, {0, 0, 0}, {10, 10, 10}},
  {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
  {{10, 10, 10}, {0, 0, 0}, {0, 0, 0}},
  {{10, 10, 10}, {10, 10, 10}, {0, 0, 0}},
  {{10, 10, 10}, {10, 10, 10}, {10, 10, 10}},
  {{0, 0, 0}, {10, 10, 10}, {10, 10, 10}},
  {{0, 0, 0}, {0, 0, 0}, {10, 10, 10}},
  {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
  {{10, 10, 10}, {0, 0, 0}, {0, 0, 0}},
  {{10, 10, 10}, {10, 10, 10}, {0, 0, 0}},
  {{10, 10, 10}, {10, 10, 10}, {10, 10, 10}},
  {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
  {{0, 10, 0}, {0, 10, 0}, {0, 10, 0}},
  {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
  {{0, 10, 0}, {0, 10, 0}, {0, 10, 0}},
};
Adafruit_NeoPixel leds = Adafruit_NeoPixel(N_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);

  rfidReader.begin(9600);
  rfidReader.listen();

  rfidPreviousMillis = millis();
  loadingStepPreviousMillis = millis();

  leds.begin();
}

void pushEvent(String category) {
  StaticJsonDocument<JSON_OBJECT_SIZE(2)> event;

  event[PROTOCOL_CATEGORY] = category;

  serializeJson(event, Serial);
  Serial.println();
}

void checkRFID() {
  currentMillis = millis();

  if (rfidReader.available() > 0) {
    rfidReader.read();
    if (!isSomethingBeingSent) {
      isSomethingBeingSent = true;
    }
    rfidPreviousMillis = currentMillis;
  }

  if (isSomethingBeingSent && currentMillis - rfidPreviousMillis >= RFID_TIME_THRESHOLD) {
    isSomethingBeingSent = false;
    pushEvent(PROTOCOL_CANCEL_AUTHENTICATION);
  }
}

void updateLeds() {
  if (isSomethingBeingSent) {
    loading = true;
  } else {
    loading = false;
    loadingStep = 0;
  }

  for (int j = 0 ; j < 3 ; j++) {
    if (status == "success") {
      leds.setPixelColor(ledIndexes[j], leds.Color(0, 10, 0));
    } else if (status == "playing") {
      if (loading) {
        leds.setPixelColor(ledIndexes[j], leds.Color(
          loadingSteps[loadingStep][j][0],
          loadingSteps[loadingStep][j][1],
          loadingSteps[loadingStep][j][2]
        ));

        if (loadingStep < LOADING_STEPS - 1) {
          currentMillis = millis();

          if (currentMillis - loadingStepPreviousMillis >= LOADING_STEPS_DELAY) {
            loadingStep++;
            loadingStepPreviousMillis = currentMillis;
          }

          if (loadingStep == LOADING_STEPS - 1) {
            pushEvent(PROTOCOL_AUTHENTICATE);
          }
        }
      } else {
        leds.setPixelColor(ledIndexes[j], leds.Color(10, 1, 0));
      }
    } else {
      // status == "disabled"
      leds.setPixelColor(ledIndexes[j], leds.Color(10, 0, 0));
    }
  }

  leds.show();
}

void loop() {
  if (status == "playing") {
    checkRFID();
  }

  updateLeds();
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

    if (category == PROTOCOL_STATUS_PLAYING) {
      status = "playing";
    } else if (category == PROTOCOL_STATUS_DISABLED) {
      isSomethingBeingSent = false;
      loadingStep = 0;
      status = "disabled";
    } else if (category == PROTOCOL_STATUS_SUCCESS) {
      isSomethingBeingSent = false;
      loadingStep = 0;
      status = "success";
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
