#include <Servo.h>
#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"
#define PROTOCOL_ERROR "e"
#define PROTOCOL_PATTERN "p"
#define PROTOCOL_PATTERN_MASK "pm"

#define PUSH_SERVO_POSITION_0 0
#define PUSH_SERVO_POSITION_1 90

#define LOCK_SERVO_POSITION_0 0
#define LOCK_SERVO_POSITION_1 95

#define PUSH_LOCK_DELAY 100

#define PATTERN_POINTS 9

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

Servo pushServos[PATTERN_POINTS];
Servo lockServos[PATTERN_POINTS];

int pushServoPins[PATTERN_POINTS] = {30, 32, 34, 36, 38, 40, 42, 44, 46};
int lockServoPins[PATTERN_POINTS] = {31, 33, 35, 37, 39, 41, 43, 45, 47};

void setup() {
  Serial.begin(9600);

  for (int i = 0 ; i < PATTERN_POINTS ; i++) {
    pushServos[i].attach(pushServoPins[i]);
    pushServos[i].write(PUSH_SERVO_POSITION_0);
    lockServos[i].attach(lockServoPins[i]);
    lockServos[i].write(LOCK_SERVO_POSITION_0);
  }
}

void loop() {}

void displayPattern(int patternMask) {
  int pointBit;

  for (int i = 0 ; i < PATTERN_POINTS ; i++) {
    pointBit = (int) pow(2, i);
    if ((pointBit & patternMask) == pointBit) {
      pushServos[i].write(PUSH_SERVO_POSITION_1);
    } else {
      lockServos[i].write(LOCK_SERVO_POSITION_0);
    }
  }

  delay(PUSH_LOCK_DELAY);

  for (int i = 0 ; i < PATTERN_POINTS ; i++) {
    pointBit = (int) pow(2, i);
    if ((pointBit & patternMask) == pointBit) {
      lockServos[i].write(LOCK_SERVO_POSITION_1);
    } else {
      pushServos[i].write(PUSH_SERVO_POSITION_0);
    }
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

    if (category == PROTOCOL_PATTERN) {
      int patternMask = receivedDocument[PROTOCOL_PATTERN_MASK];
      displayPattern(patternMask);
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
