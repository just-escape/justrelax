#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_SET_TARGET_FREQ "t"
#define PROTOCOL_SET_FREQ "f"
#define PROTOCOL_VALUE "v"
#define PROTOCOL_STEP "s"

byte PIN = 2;
float light_pwm = 0;
float light_freq = 0;
float light_target_freq = 0;
float light_target_freq_step = 0;

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

void setup() {
  pinMode(PIN, OUTPUT);

  Serial.begin(9600);

  delay(100);
}

void loop() {
  if (light_freq > light_target_freq) {
    if (light_target_freq_step == 0) {
      // Just in case a transition that was not planned is triggered
      light_freq -= 0.1;
    } else {
      light_freq -= light_target_freq_step;
    }
  } else if (light_freq < light_target_freq) {
    if (light_target_freq_step == 0) {
      // Just in case a transition that was not planned is triggered
      light_freq += 0.1;
    } else {
      light_freq += light_target_freq_step;
    }
  }

  light_pwm = 0;

  if (light_freq > 0) {
    digitalWrite(PIN, HIGH);
  }

  for (int cycle = 0 ; cycle < 50 ; cycle++) {
    if (light_pwm < light_freq) {
      light_pwm++;
    } else {
      digitalWrite(PIN, LOW);
    }

    delayMicroseconds(100);
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

    if (category == PROTOCOL_SET_TARGET_FREQ) {
      float value = receivedDocument[PROTOCOL_VALUE];
      float step = receivedDocument[PROTOCOL_STEP];
      light_target_freq = value;
      light_target_freq_step = step;
    } else if (category == PROTOCOL_SET_FREQ) {
      float value = receivedDocument[PROTOCOL_VALUE];
      light_freq = value;
      light_target_freq = value;
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
