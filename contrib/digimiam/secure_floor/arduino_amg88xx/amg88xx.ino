#include <Melopero_AMG8833.h>
#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

// Sent events
#define PROTOCOL_ERROR "e"
#define PROTOCOL_MAX "m"

// Received events
#define PROTOCOL_CALIBRATE "c"
#define PROTOCOL_CALIBRATION_SAMPLES "s"
#define PROTOCOL_CALIBRATION_DELAY "d"

#define PROTOCOL_SET_ACQUISITION_PARAMS "ap"
#define PROTOCOL_ACQUISITION_SAMPLES "as"
#define PROTOCOL_ACQUISITION_DELAY "ad"
#define PROTOCOL_INTER_ACQUISITION_DELAY "iad"

#define DEFAULT_CALIBRATION_SAMPLES 10
#define DEFAULT_CALIBRATION_DELAY 100

Melopero_AMG8833 sensor;

int i, j, k;
float calibrationMatrix[8][8];
float acquisitionMatrix[8][8];
int interAcquisitionDelay = 1000;
int acquisitionDelay = 0;
int acquisitionSamples = 1;

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

void pushMax() {
  StaticJsonDocument<JSON_OBJECT_SIZE(2)> event;

  float max = 0;
  for (i = 0 ; i < 8 ; i++) {
    for (j = 0 ; j < 8 ; j++) {
      if ((i == 0 && j == 0) || acquisitionMatrix[j][i] > max) {
        max = acquisitionMatrix[j][i];
      }
    }
  }

  event[PROTOCOL_MAX] = max;
  event[PROTOCOL_CATEGORY] = PROTOCOL_MAX;

  serializeJson(event, Serial);
  Serial.println();
}

void calibrate(int calibrationSamples, int calibrationDelay) {
  for (i = 0 ; i < 8 ; i++) {
    for (j = 0 ; j < 8 ; j++) {
      calibrationMatrix[j][i] = 0;
    }
  }

  for (k = 0 ; k < calibrationSamples ; k++) {
    sensor.updateThermistorTemperature();
    sensor.updatePixelMatrix();

    for (i = 0 ; i < 8 ; i++) {
      for (j = 0 ; j < 8 ; j++) {
        calibrationMatrix[j][i] += sensor.pixelMatrix[j][i];
      }
    }

    delay(calibrationDelay);
  }

  for (i = 0 ; i < 8 ; i++) {
    for (j = 0 ; j < 8 ; j++) {
      calibrationMatrix[j][i] = calibrationMatrix[j][i] / calibrationSamples;
    }
  }
}

void acquire(int acquisitionSamples, int acquisitionDelay) {
  for (i = 0 ; i < 8 ; i++) {
    for (j = 0 ; j < 8 ; j++) {
      acquisitionMatrix[j][i] = 0;
    }
  }

  for (k = 0 ; k < acquisitionSamples ; k++) {
    sensor.updateThermistorTemperature();
    sensor.updatePixelMatrix();

    for (i = 0 ; i < 8 ; i++) {
      for (j = 0 ; j < 8 ; j++) {
        acquisitionMatrix[j][i] += sensor.pixelMatrix[j][i] - calibrationMatrix[j][i];
      }
    }

    if (acquisitionSamples > 1) {
      delay(acquisitionDelay);
    }
  }

  if (acquisitionSamples > 1) {
    for (i = 0 ; i < 8 ; i++) {
      for (j = 0 ; j < 8 ; j++) {
        acquisitionMatrix[j][i] = acquisitionMatrix[j][i] / acquisitionSamples;
      }
    }
  }
}

void setup() {
  Serial.begin(9600);

  delay(1000);
  sensor.resetFlagsAndSettings();
  sensor.setFPSMode(FPS_MODE::FPS_10);

  delay(1000);
  calibrate(DEFAULT_CALIBRATION_SAMPLES, DEFAULT_CALIBRATION_DELAY);
}

void loop() {
  acquire(acquisitionSamples, acquisitionDelay);
  pushMax();

  delay(interAcquisitionDelay);
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

    if (category == PROTOCOL_CALIBRATE) {
      int calibrationSamples = receivedDocument[PROTOCOL_CALIBRATION_SAMPLES];
      int calibrationDelay = receivedDocument[PROTOCOL_CALIBRATION_DELAY];
      calibrate(calibrationSamples, calibrationDelay);
    } else if (category == PROTOCOL_SET_ACQUISITION_PARAMS) {
      acquisitionSamples = receivedDocument[PROTOCOL_ACQUISITION_SAMPLES];
      acquisitionDelay = receivedDocument[PROTOCOL_ACQUISITION_DELAY];
      interAcquisitionDelay = receivedDocument[PROTOCOL_INTER_ACQUISITION_DELAY];
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
