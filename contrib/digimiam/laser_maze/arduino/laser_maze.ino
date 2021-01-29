#include <ArduinoJson.h>
#include <SoftwareSerial.h>
#include <Adafruit_NeoPixel.h>

#define PROTOCOL_CATEGORY "c"

// Sent events
#define PROTOCOL_ERROR "e"
#define PROTOCOL_ALARM "a"
#define PROTOCOL_ALARM_LASER_INDEX "i"
#define PROTOCOL_TAG "t"
#define PROTOCOL_TAG_VALUE "v"
#define PROTOCOL_TAG_READER_INDEX "i"

// Received events
#define PROTOCOL_LASER_ON "l"
#define PROTOCOL_LASER_ON_BITMASK "b"
#define PROTOCOL_DYNAMIC_LASER_ON_BITMASK "d"
#define PROTOCOL_DYNAMIC_LASER_UPTIME "p"
#define PROTOCOL_DYNAMIC_LASER_DOWNTIME "n"
#define PROTOCOL_DYNAMIC_LASER_INCREMENTAL_OFFSET "o"
#define PROTOCOL_SAMPLE_DELAY "y"
#define PROTOCOL_STOP_PLAYING "s"
#define PROTOCOL_SET_SUCCESS "w"
#define PROTOCOL_SET_SUCCESS_VALUE "v"
#define PROTOCOL_SET_SAMPLE_DELAY "ssd"

#define N_LASERS 5
#define N_SAMPLES 10

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

bool success = false;
bool playing = false;

byte laserPins[N_LASERS] = {52, 50, 48, 46, 44};
bool isLaserOn[N_LASERS] = {false};
byte sensorPins[N_LASERS] = {53, 51, 49, 47, 45};
bool sensorSamples[N_LASERS][N_SAMPLES];
unsigned long sensorSamplesMillis;
unsigned long sampleDelay = 10;
byte sensorSamplesCursor = 0;

int dynamicLasers[N_LASERS] = {false};
unsigned long dynamicPreviousMillis[N_LASERS] = {0};
unsigned long dynamicLasersUptime = 7500;
unsigned long dynamicLasersDowntime = 5500;
unsigned long dynamicLasersIncrementalOffset = 300;

#define BLINK_INTERVAL 1000
unsigned long blinkPreviousMillis = 0;
byte blinkingLaser = -1;
bool blinkingLaserState = true;

bool read;
unsigned long currentMillis = 0;

#define N_READERS 2
byte softwareSerialPins[N_READERS][2] = {{10, 11}, {12, 13}};
SoftwareSerial *rfidReaders[N_READERS];
unsigned long rfidPreviousMillis[N_LASERS] = {0};
#define RFID_TIME_THRESHOLD 2000
bool isSomethingBeingSent[N_READERS] = {false};
bool pushedTag[N_READERS] = {false};

#define LED_PIN 7
#define N_LEDS 7
#define LOADING_STEPS 30
#define LOADING_STEPS_DELAY 100
byte readerLedIndexes[N_READERS][3] = {{2, 1, 0}, {3, 4, 5}};
byte loadingTag[N_READERS] = {false};
byte loadingStep[N_READERS] = {0};
unsigned long loadingStepPreviousMillis[N_READERS] = {0};
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
  for (int i = 0 ; i < N_LASERS ; i++) {
    pinMode(laserPins[i], OUTPUT);
    pinMode(sensorPins[i], INPUT);
  }

  Serial.begin(9600);

  for (int i = 0 ; i < N_READERS ; i++) {
    rfidReaders[i] = new SoftwareSerial(softwareSerialPins[i][0], softwareSerialPins[i][1]);
    rfidReaders[i]->begin(9600);
    rfidPreviousMillis[i] = millis();
    isSomethingBeingSent[i] = false;
    loadingTag[i] = false;
    pushedTag[i] = false;
    loadingStep[i] = 0;
    loadingStepPreviousMillis[i] = millis();
  }

  sensorSamplesMillis = millis();

  leds.begin();
}

void alarm(int laserIndex) {
  playing = false;
  blinkingLaser = laserIndex;
  blinkingLaserState = true;

  for (int i = 0 ; i < N_LASERS ; i++) {
    if (i != laserIndex) {
      digitalWrite(laserPins[i], LOW);
    }
  }

  StaticJsonDocument<JSON_OBJECT_SIZE(2)> event;

  event[PROTOCOL_CATEGORY] = PROTOCOL_ALARM;
  event[PROTOCOL_ALARM_LASER_INDEX] = laserIndex;

  serializeJson(event, Serial);
  Serial.println();
}

void blinkLaser() {
  if (blinkingLaser != -1) {
    currentMillis = millis();
    if (currentMillis - blinkPreviousMillis >= BLINK_INTERVAL) {
      blinkPreviousMillis = currentMillis;
      blinkingLaserState = !blinkingLaserState;
      digitalWrite(laserPins[blinkingLaser], blinkingLaserState);
    }
  }
}

void checkSensors() {
  bool isAlarmConfirmed;

  currentMillis = millis();

  if (currentMillis - sensorSamplesMillis >= sampleDelay) {
    for (int i = 0 ; i < N_LASERS ; i++) {
      if (isLaserOn[i]) {
        read = digitalRead(sensorPins[i]);
        sensorSamples[i][sensorSamplesCursor] = read;

        // By default alarm is confirmed. Checking sensor samples will validate or not this supposition.
        isAlarmConfirmed = true;
        for (int j = 0 ; j < N_SAMPLES ; j++) {
          if (sensorSamples[i][j]) {
            isAlarmConfirmed = false;
            break;
          }
        }

        if (isAlarmConfirmed) {
          alarm(i);
          return;
        }
      }
    }

    sensorSamplesCursor = (sensorSamplesCursor + 1) % N_SAMPLES;
    sensorSamplesMillis = currentMillis;
  }
}

void updateDynamicLasers() {
  currentMillis = millis();

  unsigned long incrementalOffset = 0;
  for (int i = 0 ; i < N_LASERS ; i++) {
    if (dynamicLasers[i]) {
      if (
          (isLaserOn[i] && currentMillis - dynamicPreviousMillis[i] >= dynamicLasersUptime + incrementalOffset) ||
          (!isLaserOn[i] && currentMillis - dynamicPreviousMillis[i] >= dynamicLasersDowntime + incrementalOffset)
      ) {
        isLaserOn[i] = !isLaserOn[i];
        digitalWrite(laserPins[i], isLaserOn[i]);
        dynamicPreviousMillis[i] = currentMillis - incrementalOffset;

        if (!isLaserOn[i]) {
          for (int j = 0 ; j < N_SAMPLES ; j++) {
            sensorSamples[i][j] = true;
          }
        }
      }

      incrementalOffset += dynamicLasersIncrementalOffset;
    }
  }
}

void pushBool(bool v, int i) {
  StaticJsonDocument<JSON_OBJECT_SIZE(3)> event;

  event[PROTOCOL_CATEGORY] = PROTOCOL_TAG;
  event[PROTOCOL_TAG_VALUE] = v;
  event[PROTOCOL_TAG_READER_INDEX] = i;

  serializeJson(event, Serial);
  Serial.println();
}

void checkRFID() {
  for (int i = 0 ; i < N_READERS ; i++) {
    currentMillis = millis();

    rfidReaders[i]->listen();

    if (rfidReaders[i]->available() > 0) {
      if (!isSomethingBeingSent[i]) {
        isSomethingBeingSent[i] = true;
      }
      rfidPreviousMillis[i] = currentMillis;
    }

    if (isSomethingBeingSent[i] && currentMillis - rfidPreviousMillis[i] >= RFID_TIME_THRESHOLD) {
      isSomethingBeingSent[i] = false;
      pushedTag[i] = false;
      pushBool(false, i);
    }
  }
}

void updateLeds() {
  for (int i = 0 ; i < N_READERS ; i++) {
    if (isSomethingBeingSent[i]) {
      loadingTag[i] = true;
    } else {
      loadingTag[i] = false;
      loadingStep[i] = 0;
    }

    for (int j = 0 ; j < 3 ; j++) {
      if (success) {
        leds.setPixelColor(readerLedIndexes[i][j], leds.Color(0, 10, 0));
      } else if (!playing) {
        leds.setPixelColor(readerLedIndexes[i][j], leds.Color(10, 0, 0));
      } else if (loadingTag[i] && loadingStep[i] < LOADING_STEPS - 1) {
        leds.setPixelColor(readerLedIndexes[i][j], leds.Color(
          loadingSteps[loadingStep[i]][j][0],
          loadingSteps[loadingStep[i]][j][1],
          loadingSteps[loadingStep[i]][j][2]
        ));

        currentMillis = millis();

        if (currentMillis - loadingStepPreviousMillis[i] >= LOADING_STEPS_DELAY) {
          loadingStep[i]++;
          loadingStepPreviousMillis[i] = currentMillis;
        }
      } else if (isSomethingBeingSent[i]) {
        leds.setPixelColor(readerLedIndexes[i][j], leds.Color(0, 10, 0));

        if (!pushedTag[i]) {
          pushedTag[i] = true;
          pushBool(true, i);
        }
      } else if (playing) {
        leds.setPixelColor(readerLedIndexes[i][j], leds.Color(10, 1, 0));
      }
    }
  }

  leds.show();
}

void loop() {
  if (!success && playing) {
    updateDynamicLasers();
    checkSensors();
    checkRFID();
  } else {
    blinkLaser();
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

    if (category == PROTOCOL_STOP_PLAYING) {
      playing = false;

      for (int i = 0 ; i < N_READERS ; i++) {
        isSomethingBeingSent[i] = false;
        pushedTag[i] = false;
        pushBool(false, i);
      }

      for (int i = 0 ; i < N_LASERS ; i++) {
        if (i != blinkingLaser) {
          isLaserOn[i] = false;
          digitalWrite(laserPins[i], LOW);
        }
      }
    } else if (category == PROTOCOL_SET_SUCCESS) {
      success = receivedDocument[PROTOCOL_SET_SUCCESS_VALUE];

      blinkingLaser = -1;

      for (int i = 0 ; i < N_READERS ; i++) {
        isSomethingBeingSent[i] = false;
        pushedTag[i] = false;
        pushBool(false, i);
      }

      for (int i = 0 ; i < N_LASERS ; i++) {
        if (i != blinkingLaser) {
          isLaserOn[i] = false;
          digitalWrite(laserPins[i], LOW);
        }
      }
    } else if (category == PROTOCOL_LASER_ON) {
      JsonVariant uncastBitmask = receivedDocument[PROTOCOL_LASER_ON_BITMASK];
      unsigned int bitmask = uncastBitmask.as<unsigned int>();
      int dynamicLasersBitmask = receivedDocument[PROTOCOL_DYNAMIC_LASER_ON_BITMASK];
      dynamicLasersUptime = receivedDocument[PROTOCOL_DYNAMIC_LASER_UPTIME];
      dynamicLasersDowntime = receivedDocument[PROTOCOL_DYNAMIC_LASER_DOWNTIME];
      dynamicLasersIncrementalOffset = receivedDocument[PROTOCOL_DYNAMIC_LASER_INCREMENTAL_OFFSET];
      sampleDelay = receivedDocument[PROTOCOL_SAMPLE_DELAY];
      currentMillis = millis();
      unsigned int currentBit = 1;

      for (int i = 0 ; i < N_LASERS ; i++) {
        isLaserOn[i] = (bitmask & currentBit) == currentBit;
        digitalWrite(laserPins[i], isLaserOn[i]);
        dynamicLasers[i] = (dynamicLasersBitmask & currentBit) == currentBit;
        dynamicPreviousMillis[i] = currentMillis;
        currentBit = currentBit << 1;

        for (int j = 0 ; j < N_SAMPLES ; j++) {
          sensorSamples[i][j] = true;
        }
      }

      playing = true;
      blinkingLaser = -1;
    } else if (category == PROTOCOL_SET_SAMPLE_DELAY) {
      sampleDelay = receivedDocument[PROTOCOL_SAMPLE_DELAY];
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