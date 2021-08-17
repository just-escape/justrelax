#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_LED_SET_COLOR_BLACK "b"
#define PROTOCOL_LED_SET_COLOR_ORANGE "o"
#define PROTOCOL_LED_SET_COLOR_RED "r"
#define PROTOCOL_LED_SET_COLOR_WHITE "w"
#define PROTOCOL_LED_STRIP_BIT_MASK "s"

#define N_STRIPS 2

byte LIGHT_RGB_PINS[N_STRIPS][3] = {{52, 50, 48}, {46, 44, 42}};
float light_rgb_pwm[N_STRIPS][3] = {{0, 0, 0}, {0, 0, 0}};
float light_rgb_freq[N_STRIPS][3] = {{0, 0, 0}, {0, 0, 0}};
float light_rgb_target_freq[N_STRIPS][3] = {{0, 0, 0}, {0, 0, 0}};
float light_rgb_target_freq_step[N_STRIPS][3] = {{0, 0, 0}, {0, 0, 0}};

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

void setup() {
  for (int i = 0 ; i < N_STRIPS ; i++) {
    pinMode(LIGHT_RGB_PINS[i][0], OUTPUT);
    pinMode(LIGHT_RGB_PINS[i][1], OUTPUT);
    pinMode(LIGHT_RGB_PINS[i][2], OUTPUT);
  }

  Serial.begin(9600);

  delay(100);
}

void loop() {
  for (int i = 0 ; i < N_STRIPS ; i++) {
    for (int j = 0 ; j < 3 ; j++) {
      if (light_rgb_freq[i][j] > light_rgb_target_freq[i][j]) {
        if (light_rgb_target_freq_step[i][j] == 0) {
          // Just in case a transition that was not planned is triggered
          light_rgb_freq[i][j] -= 0.1;
        } else {
          light_rgb_freq[i][j] -= light_rgb_target_freq_step[i][j];
        }
      } else if (light_rgb_freq[i][j] < light_rgb_target_freq[i][j]) {
        if (light_rgb_target_freq_step[i][j] == 0) {
          // Just in case a transition that was not planned is triggered
          light_rgb_freq[i][j] += 0.1;
        } else {
          light_rgb_freq[i][j] += light_rgb_target_freq_step[i][j];
        }
      }
    }
  }

  for (int i = 0 ; i < N_STRIPS ; i++) {
    for (int j = 0 ; j < 3 ; j++) {
      light_rgb_pwm[i][j] = 0;

      if (light_rgb_freq[i][j] > 0) {
        digitalWrite(LIGHT_RGB_PINS[i][j], HIGH);
      }
    }
  }

  for (int cycle = 0 ; cycle < 50 ; cycle++) {
    for (int i = 0 ; i < N_STRIPS ; i++) {
      for (int j = 0 ; j < 3 ; j++) {
        if (light_rgb_pwm[i][j] < light_rgb_freq[i][j]) {
          light_rgb_pwm[i][j]++;
        } else {
          digitalWrite(LIGHT_RGB_PINS[i][j], LOW);
        }
      }
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
    int led_strip_bit_mask = receivedDocument[PROTOCOL_LED_STRIP_BIT_MASK];
    int current_strip_bit = 1;

    if (category == PROTOCOL_LED_SET_COLOR_BLACK) {
      for (int i = 0 ; i < N_STRIPS ; i++) {
        if ((led_strip_bit_mask & current_strip_bit) == current_strip_bit) {
          light_rgb_freq[i][0] = 0;
          light_rgb_freq[i][1] = 0;
          light_rgb_freq[i][2] = 0;
          light_rgb_target_freq[i][0] = 0;
          light_rgb_target_freq[i][1] = 0;
          light_rgb_target_freq[i][2] = 0;
        }
        current_strip_bit = current_strip_bit << 1;
      }
    } else if (category == PROTOCOL_LED_SET_COLOR_ORANGE) {
      for (int i = 0 ; i < N_STRIPS ; i++) {
        if ((led_strip_bit_mask & current_strip_bit) == current_strip_bit) {
          light_rgb_target_freq[i][0] = 20;
          light_rgb_target_freq[i][1] = 4;
          light_rgb_target_freq[i][2] = 0;
          light_rgb_target_freq_step[i][0] = 1;
          light_rgb_target_freq_step[i][1] = 0.2;
          light_rgb_target_freq_step[i][2] = 0;
        }
        current_strip_bit = current_strip_bit << 1;
      }
    } else if (category == PROTOCOL_LED_SET_COLOR_RED) {
      for (int i = 0 ; i < N_STRIPS ; i++) {
        if ((led_strip_bit_mask & current_strip_bit) == current_strip_bit) {
          light_rgb_target_freq[i][0] = 50;
          light_rgb_target_freq[i][1] = 0;
          light_rgb_target_freq[i][2] = 0;
          light_rgb_target_freq_step[i][0] = 0.4;
          light_rgb_target_freq_step[i][1] = 0.2;
          light_rgb_target_freq_step[i][2] = 0;
        }
        current_strip_bit = current_strip_bit << 1;
      }
    } else if (category == PROTOCOL_LED_SET_COLOR_WHITE) {
      for (int i = 0 ; i < N_STRIPS ; i++) {
        if ((led_strip_bit_mask & current_strip_bit) == current_strip_bit) {
          light_rgb_target_freq[i][0] = 50;
          light_rgb_target_freq[i][1] = 50;
          light_rgb_target_freq[i][2] = 50;
          light_rgb_target_freq_step[i][0] = 0.5;
          light_rgb_target_freq_step[i][1] = 0.5;
          light_rgb_target_freq_step[i][2] = 0.5;
        }
        current_strip_bit = current_strip_bit << 1;
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
