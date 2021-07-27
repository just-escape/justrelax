#include <ArduinoJson.h>
#include <SoftwareSerial.h>
#include <Adafruit_NeoPixel.h>

const int BUFFER_SIZE = 14; // RFID DATA FRAME FORMAT: 1byte head (value: 2), 10byte data (2byte version + 8byte tag), 2byte checksum, 1byte tail (value: 3)
const int DATA_SIZE = 10; // 10byte data (2byte version + 8byte tag)
const int DATA_VERSION_SIZE = 2; // 2byte version (actual meaning of these two bytes may vary)
const int DATA_TAG_SIZE = 8; // 8byte tag
const int CHECKSUM_SIZE = 2; // 2byte checksum

uint8_t buffer[BUFFER_SIZE]; // used to store an incoming data frame
int buffer_index = 0;
unsigned lastReadTag;

#define PROTOCOL_CATEGORY "c"

// Sent events
#define PROTOCOL_ERROR "e"
#define PROTOCOL_AUTHENTICATE "a"
#define PROTOCOL_CANCEL_AUTHENTICATION "c"
#define PROTOCOL_TAG "t"

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
#define RFID_TIME_THRESHOLD 3000

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
  StaticJsonDocument<JSON_OBJECT_SIZE(4)> event;

  event[PROTOCOL_CATEGORY] = category;
  event[PROTOCOL_TAG] = lastReadTag;

  serializeJson(event, Serial);
  Serial.println();
}

long hexstr_to_value(char *str, unsigned int length) { // converts a hexadecimal value (encoded as ASCII string) to a numeric value
  char* copy = malloc((sizeof(char) * length) + 1);
  memcpy(copy, str, sizeof(char) * length);
  copy[length] = '\0';
  // the variable "copy" is a copy of the parameter "str". "copy" has an additional '\0' element to make sure that "str" is null-terminated.
  long value = strtol(copy, NULL, 16);  // strtol converts a null-terminated string to a long value
  free(copy); // clean up
  return value;
}

unsigned extract_tag() {
    uint8_t msg_head = buffer[0];
    uint8_t *msg_data = buffer + 1; // 10 byte => data contains 2byte version + 8byte tag
    uint8_t *msg_data_version = msg_data;
    uint8_t *msg_data_tag = msg_data + 2;
    uint8_t *msg_checksum = buffer + 11; // 2 byte
    uint8_t msg_tail = buffer[13];

    // print message that was sent from RDM630/RDM6300
    // Serial.println("--------");

    // Serial.print("Message-Head: ");
    // Serial.println(msg_head);

    // Serial.println("Message-Data (HEX): ");
    // for (int i = 0; i < DATA_VERSION_SIZE; ++i) {
    //   Serial.print(char(msg_data_version[i]));
    // }
    // Serial.println(" (version)");
    // for (int i = 0; i < DATA_TAG_SIZE; ++i) {
    //   Serial.print(char(msg_data_tag[i]));
    // }
    // Serial.println(" (tag)");

    // Serial.print("Message-Checksum (HEX): ");
    // for (int i = 0; i < CHECKSUM_SIZE; ++i) {
    //   Serial.print(char(msg_checksum[i]));
    // }
    // Serial.println("");

    // Serial.print("Message-Tail: ");
    // Serial.println(msg_tail);

    // Serial.println("--");

    long tag = hexstr_to_value(msg_data_tag, DATA_TAG_SIZE);
    // Serial.print("Extracted Tag: ");
    // Serial.println(tag);

    long checksum = 0;
    for (int i = 0; i < DATA_SIZE; i+= CHECKSUM_SIZE) {
      long val = hexstr_to_value(msg_data + i, CHECKSUM_SIZE);
      checksum ^= val;
    }
    // Serial.print("Extracted Checksum (HEX): ");
    // Serial.print(checksum, HEX);
    // if (checksum == hexstr_to_value(msg_checksum, CHECKSUM_SIZE)) { // compare calculated checksum to retrieved checksum
    //   Serial.print(" (OK)"); // calculated checksum corresponds to transmitted checksum!
    // } else {
    //   Serial.print(" (NOT OK)"); // checksums do not match
    // }

    // Serial.println("");
    // Serial.println("--------");

    return tag;
}

void checkRFID() {
  currentMillis = millis();

  if (rfidReader.available() > 0) {
    bool call_extract_tag = false;

    int ssvalue = rfidReader.read(); // read
    if (ssvalue == -1) { // no data was read
      return;
    }

    if (ssvalue == 2) { // RDM630/RDM6300 found a tag => tag incoming
      isSomethingBeingSent = true;
      rfidPreviousMillis = currentMillis;
      buffer_index = 0;
    } else if (ssvalue == 3) { // tag has been fully transmitted
      call_extract_tag = true; // extract tag at the end of the function call
    }

    if (buffer_index >= BUFFER_SIZE) { // checking for a buffer overflow (It's very unlikely that an buffer overflow comes up!)
      // Serial.println("Error: Buffer overflow detected!");
      return;
    }

    buffer[buffer_index++] = ssvalue; // everything is alright => copy current value to buffer

    if (call_extract_tag == true) {
      if (buffer_index == BUFFER_SIZE) {
        lastReadTag = extract_tag();
      } else { // something is wrong... start again looking for preamble (value: 2)
        buffer_index = 0;
        return;
      }
    }
  }

  if (isSomethingBeingSent && currentMillis - rfidPreviousMillis >= RFID_TIME_THRESHOLD) {
    isSomethingBeingSent = false;
    pushEvent(PROTOCOL_CANCEL_AUTHENTICATION);
    lastReadTag = 0;  // Not supposed to matter but...
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
        leds.setPixelColor(ledIndexes[j], leds.Color(10, 10, 10));
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
