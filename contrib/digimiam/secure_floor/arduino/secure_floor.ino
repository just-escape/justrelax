#include <HX711-multi.h>
#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_TARE "t"

#define PROTOCOL_LED_SET_COLOR_BLACK "b"
#define PROTOCOL_LED_SET_COLOR_ORANGE "o"
#define PROTOCOL_LED_SET_COLOR_RED "r"
#define PROTOCOL_LED_SET_COLOR_WHITE "w"

#define HX711_CLK 2
#define HX711_N_CELLS 2
byte HX711_DOUT_PINS[2] = {3, 4};
long int hx711Measures[2];
HX711MULTI hx711Scales(2, HX711_DOUT_PINS, HX711_CLK);

byte LIGHT_RGB_PINS[HX711_N_CELLS][3] = {{52, 50, 48}, {46, 44, 42}};
float light_rgb_pwm[HX711_N_CELLS][3] = {{0, 0, 0}, {0, 0, 0}};
float light_rgb_freq[HX711_N_CELLS][3] = {{0, 0, 0}, {0, 0, 0}};
float light_rgb_target_freq[HX711_N_CELLS][3] = {{0, 0, 0}, {0, 0, 0}};
float light_rgb_target_freq_step[HX711_N_CELLS][3] = {{0, 0, 0}, {0, 0, 0}};

int scales_temporizer = 0;

byte OUTPUT_PINS[2] = {5, 6};

#define THRESHOLD 1

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

void hx711_tare() {
  bool isTareSuccessful = false;
  unsigned long tareTimeout = 4000;

  unsigned long tareStartTime = millis();
  while (!isTareSuccessful && millis() < (tareStartTime + tareTimeout)) {
    isTareSuccessful = hx711Scales.tare(20, 10000);
  }
}

void setup() {
  hx711_tare();

  for (int i = 0 ; i < HX711_N_CELLS ; i++) {
    pinMode(LIGHT_RGB_PINS[i][0], OUTPUT);
    pinMode(LIGHT_RGB_PINS[i][1], OUTPUT);
    pinMode(LIGHT_RGB_PINS[i][2], OUTPUT);
  }

  Serial.begin(9600);

  delay(100);
}

int tmp = 0;

void loop() {
  if (tmp == 500) {
    for (int i = 0 ; i < 2 ; i++) {
          light_rgb_target_freq[i][0] = 50;
          light_rgb_target_freq[i][1] = 10;
          light_rgb_target_freq[i][2] = 0;
          light_rgb_target_freq_step[i][0] = 0.5;
          light_rgb_target_freq_step[i][1] = 0.1;
          light_rgb_target_freq_step[i][2] = 0;
    }
  } else {
    tmp++;
  }

  for (int i = 0 ; i < HX711_N_CELLS ; i++) {
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

  for (int i = 0 ; i < HX711_N_CELLS ; i++) {
    for (int j = 0 ; j < 3 ; j++) {
      light_rgb_pwm[i][j] = 0;

      if (light_rgb_freq[i][j] > 0) {
        digitalWrite(LIGHT_RGB_PINS[i][j], HIGH);
      }
    }
  }

  for (int cycle = 0 ; cycle < 50 ; cycle++) {
    for (int i = 0 ; i < HX711_N_CELLS ; i++) {
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

  /*if (scales_temporizer < 10) {
    scales_temporizer++;
  } else {
    hx711Scales.read(hx711Measures);
    for (int i = 0 ; i < hx711Scales.get_count() ; i++) {
      if (hx711Measures[i] / 40000 >= THRESHOLD) {
        digitalWrite(OUTPUT_PINS[i], HIGH);
        if (light_rgb_target_freq[i][0] == 0 && light_rgb_target_freq[i][1] == 0 && light_rgb_target_freq[i][2] == 0) {
          light_rgb_target_freq[i][0] = 50;
          light_rgb_target_freq[i][1] = 10;
          light_rgb_target_freq[i][2] = 0;
          light_rgb_target_freq_step[i][0] = 1;
          light_rgb_target_freq_step[i][1] = 0.2;
          light_rgb_target_freq_step[i][2] = 0;
        }
      } else {
        digitalWrite(OUTPUT_PINS[i], LOW);
      }
    }
    scales_temporizer = 0;
  }*/
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

    if (category == PROTOCOL_LED_SET_COLOR_BLACK) {
      for (int i = 0 ; i < HX711_N_CELLS ; i++) {
        light_rgb_target_freq[i][0] = 0;
        light_rgb_target_freq[i][1] = 0;
        light_rgb_target_freq[i][2] = 0;
        light_rgb_target_freq_step[i][0] = 0.1;
        light_rgb_target_freq_step[i][1] = 0.1;
        light_rgb_target_freq_step[i][2] = 0.1;
      }
    } else if (category == PROTOCOL_LED_SET_COLOR_ORANGE) {
      for (int i = 0 ; i < HX711_N_CELLS ; i++) {
        light_rgb_target_freq[i][0] = 50;
        light_rgb_target_freq[i][1] = 10;
        light_rgb_target_freq[i][2] = 0;
        light_rgb_target_freq_step[i][0] = 1;
        light_rgb_target_freq_step[i][1] = 0.2;
        light_rgb_target_freq_step[i][2] = 0;
      }
    } else if (category == PROTOCOL_LED_SET_COLOR_RED) {
      for (int i = 0 ; i < HX711_N_CELLS ; i++) {
        light_rgb_target_freq[i][0] = 50;
        light_rgb_target_freq[i][1] = 0;
        light_rgb_target_freq[i][2] = 0;
        light_rgb_target_freq_step[i][0] = 0;
        light_rgb_target_freq_step[i][1] = 0.4;
        light_rgb_target_freq_step[i][2] = 0;
      }
    } else if (category == PROTOCOL_LED_SET_COLOR_WHITE) {
      for (int i = 0 ; i < HX711_N_CELLS ; i++) {
        for (int j = 0 ; j < 3 ; j++) {
          light_rgb_target_freq[i][j] = 50;
        }
        light_rgb_target_freq_step[i][0] = 0;
        light_rgb_target_freq_step[i][1] = 0.4;
        light_rgb_target_freq_step[i][2] = 0.5;
      }
    } else if (category == PROTOCOL_TARE) {
      hx711_tare();
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
