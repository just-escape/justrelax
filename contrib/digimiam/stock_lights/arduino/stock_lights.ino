#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_WHITE_HIGH "b"
#define PROTOCOL_WHITE_LOW "o"
#define PROTOCOL_WHITE_OFF "r"

byte LIGHT_RGB_PIN = 48;
float light_rgb_pwm = 0;
float light_rgb_freq = 0;
float light_rgb_target_freq = 0;
float light_rgb_target_freq_step = 0;

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

void setup() {
  pinMode(LIGHT_RGB_PIN, OUTPUT);

  Serial.begin(9600);

  delay(100);
}

void loop() {
  if (light_rgb_freq > light_rgb_target_freq) {
    if (light_rgb_target_freq_step == 0) {
      // Just in case a transition that was not planned is triggered
      light_rgb_freq -= 0.1;
    } else {
      light_rgb_freq -= light_rgb_target_freq_step;
    }
  } else if (light_rgb_freq < light_rgb_target_freq) {
    if (light_rgb_target_freq_step == 0) {
      // Just in case a transition that was not planned is triggered
      light_rgb_freq += 0.1;
    } else {
      light_rgb_freq += light_rgb_target_freq_step;
    }
  }

  light_rgb_pwm = 0;

  if (light_rgb_freq > 0) {
    digitalWrite(LIGHT_RGB_PIN, HIGH);
  }

  for (int cycle = 0 ; cycle < 50 ; cycle++) {
    if (light_rgb_pwm < light_rgb_freq) {
      light_rgb_pwm++;
    } else {
      digitalWrite(LIGHT_RGB_PIN, LOW);
    }

    delayMicroseconds(200);
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

    if (category == PROTOCOL_WHITE_HIGH) {
      light_rgb_target_freq = 0;
      light_rgb_target_freq_step = 0;
    } else if (category == PROTOCOL_WHITE_LOW) {
      light_rgb_target_freq = 0;
      light_rgb_target_freq_step = 0;
    } else if (category == PROTOCOL_WHITE_OFF) {
      light_rgb_target_freq = 0;
      light_rgb_target_freq_step = 0;
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
