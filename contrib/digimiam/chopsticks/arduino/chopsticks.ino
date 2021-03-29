#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"
#define PROTOCOL_STATUS_PLAYING "p"
#define PROTOCOL_STATUS_SUCCESS "w"
#define PROTOCOL_CONFIGURE "c"
#define PROTOCOL_CONFIGURE_PERMA_BLUE_LEDS "b"
#define PROTOCOL_CONFIGURE_PERMA_ORANGE_LEDS "o"

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

String status = "playing";
#define STRIP_MAX_LENGTH 30
int nLeds = STRIP_MAX_LENGTH;
int permaBlueLeds = STRIP_MAX_LENGTH;
int permaOrangeLeds = 0;
#define LED_PIN 2
Adafruit_NeoPixel leds = Adafruit_NeoPixel(STRIP_MAX_LENGTH, LED_PIN, NEO_GRB + NEO_KHZ800);

unsigned long currentMillis = 0;
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(9600);

  // Configure pins 52, 50, 48, 46, 44, 42, 40
  for (int i = 0 ; i < 7 ; i++) {
    pinMode(52 - 2 * i, INPUT);
  }

  leds.begin();
}

void updateLeds() {
  currentMillis = millis();
  if (currentMillis - previousMillis >= 10) {
    previousMillis = currentMillis;

    for (int i = 0 ; i < nLeds ; i++) {
      if (i < permaBlueLeds) {
        leds.setPixelColor(i, leds.Color(0, 0, 255));
      } else if (i < permaBlueLeds + permaOrangeLeds) {
        leds.setPixelColor(i, leds.Color(255, 5, 0));
      } else {
        // Digital read on 52, 50, 48, 46, 44, 42, 40
        if (digitalRead(52 - 2 * (i - (permaBlueLeds + permaOrangeLeds)))) {
          leds.setPixelColor(i, leds.Color(0, 0, 255));
        } else {
          leds.setPixelColor(i, leds.Color(255, 5, 0));
        }
      }
    }
    leds.show();
  }
}

void loop() {
  if (status == "playing") {
    updateLeds();
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

    if (category == PROTOCOL_STATUS_PLAYING) {
      status = "playing";
    } else if (category == PROTOCOL_STATUS_SUCCESS) {
      status = "success";
    } else if (category == PROTOCOL_CONFIGURE) {
      permaBlueLeds = receivedDocument[PROTOCOL_CONFIGURE_PERMA_BLUE_LEDS];
      permaOrangeLeds = receivedDocument[PROTOCOL_CONFIGURE_PERMA_ORANGE_LEDS];

      nLeds = permaBlueLeds + permaOrangeLeds + 7;
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
