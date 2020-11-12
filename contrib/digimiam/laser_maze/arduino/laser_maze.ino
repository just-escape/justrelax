#include <ArduinoJson.h>

// https://www.mschoeffler.de/2018/01/05/arduino-tutorial-how-to-use-the-rdm630-rdm6300-rfid-reader/
#include <SoftwareSerial.h>

#define PROTOCOL_CATEGORY "c"

// Sent events
#define PROTOCOL_ERROR "e"
#define PROTOCOL_ALARM "a"
#define PROTOCOL_ALARM_LASER_INDEX "i"
#define PROTOCOL_TAG "t"
#define PROTOCOL_TAG_VALUE "v"

// Received events
#define PROTOCOL_LASER_ON "l"
#define PROTOCOL_LASER_ON_BITMASK "b"
#define PROTOCOL_STOP_PLAYING "s"

#define N_LASERS 5

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

bool playing = false;

byte laserPins[N_LASERS] = {52, 50, 48, 46, 44};
bool isLaserOn[N_LASERS] = {false};
byte sensorPins[N_LASERS] = {53, 51, 49, 47, 45};

#define BLINK_INTERVAL 1000
unsigned long previousMillis = 0;
unsigned long currentMillis = 0;
byte blinkingLaser = -1;
bool blinkingLaserState = true;

bool read;

#define RFID_BUFFER_SIZE 14
#define RFID_DATA_SIZE 10
#define RFID_DATA_VERSION_SIZE 2
#define RFID_DATA_TAG_SIZE 8
#define RFID_CHECKSUM_SIZE 2
SoftwareSerial ssrfid = SoftwareSerial(6, 8);
uint8_t rfid_buffer[RFID_BUFFER_SIZE];
int rfid_buffer_index = 0;

void setup() {
  for (int i = 0 ; i < N_LASERS ; i++) {
    pinMode(laserPins[i], OUTPUT);
    pinMode(sensorPins[i], INPUT);
  }

  Serial.begin(9600);
  ssrfid.begin(9600);
  ssrfid.listen();
}

void alarm(int laserIndex) {
  playing = false;
  blinkingLaser = laserIndex;
  blinkingLaserState = true;

  StaticJsonDocument<JSON_OBJECT_SIZE(2)> event;

  event[PROTOCOL_CATEGORY] = PROTOCOL_ALARM;
  event[PROTOCOL_ALARM_LASER_INDEX] = laserIndex;

  serializeJson(event, Serial);
  Serial.println();
}

void blinkLaser() {
  if (blinkingLaser != -1) {
    currentMillis = millis();
    if (currentMillis - previousMillis >= BLINK_INTERVAL) {
      previousMillis = currentMillis;
      blinkingLaserState = !blinkingLaserState;
      digitalWrite(laserPins[blinkingLaser], blinkingLaserState);
    }
  }
}

void checkSensors() {
  for (int i = 0 ; i < N_LASERS ; i++) {
    if (isLaserOn[i]) {
      read = digitalRead(sensorPins[i]);
      if (!read) {  // Or if read, depending on sensors
        alarm(i);
      }
    }
  }
}

// converts a hexadecimal value (encoded as ASCII string) to a numeric value
long hexstr_to_value(char *str, unsigned int length) {
  char* copy = malloc((sizeof(char) * length) + 1);
  memcpy(copy, str, sizeof(char) * length);
  copy[length] = '\0';
  // the variable "copy" is a copy of the parameter "str". "copy" has an additional '\0' element to make sure that "str" is null-terminated.
  long value = strtol(copy, NULL, 16);  // strtol converts a null-terminated string to a long value
  free(copy); // clean up
  return value;
}

unsigned extract_tag() {
    // uint8_t msg_head = rfid_buffer[0];
    uint8_t *msg_data = rfid_buffer + 1; // 10 byte => data contains 2byte version + 8byte tag
    // uint8_t *msg_data_version = msg_data;
    uint8_t *msg_data_tag = msg_data + 2;
    // uint8_t *msg_checksum = rfid_buffer + 11; // 2 byte
    // uint8_t msg_tail = rfid_buffer[13];

    // Serial.println("--------");
    // Serial.print("Message-Head: ");
    // Serial.println(msg_head);
    // Serial.println("Message-Data (HEX): ");
    // for (int i = 0; i < RFID_DATA_VERSION_SIZE; ++i) {
    //   Serial.print(char(msg_data_version[i]));
    // }
    // Serial.println(" (version)");
    // for (int i = 0; i < RFID_DATA_TAG_SIZE; ++i) {
    //   Serial.print(char(msg_data_tag[i]));
    // }
    // Serial.println(" (tag)");
    // Serial.print("Message-Checksum (HEX): ");
    // for (int i = 0; i < RFID_CHECKSUM_SIZE; ++i) {
    //   Serial.print(char(msg_checksum[i]));
    // }
    // Serial.println("");
    // Serial.print("Message-Tail: ");
    // Serial.println(msg_tail);
    // Serial.println("--");
    long tag = hexstr_to_value(msg_data_tag, RFID_DATA_TAG_SIZE);
    // Serial.print("Extracted Tag: ");
    // Serial.println(tag);
    // long checksum = 0;
    // for (int i = 0; i < RFID_DATA_SIZE; i+= RFID_CHECKSUM_SIZE) {
    //   long val = hexstr_to_value(msg_data + i, RFID_CHECKSUM_SIZE);
    //   checksum ^= val;
    // }
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

void pushTag(unsigned tag) {
  StaticJsonDocument<JSON_OBJECT_SIZE(2)> event;

  event[PROTOCOL_CATEGORY] = PROTOCOL_TAG;
  event[PROTOCOL_TAG_VALUE] = tag;

  serializeJson(event, Serial);
  Serial.println();
}

void checkRFID() {
  if (ssrfid.available() > 0) {
    bool call_extract_tag = false;

    int ssvalue = ssrfid.read(); // read
    if (ssvalue == -1) { // no data was read
      return;
    }
    if (ssvalue == 2) { // RDM630/RDM6300 found a tag => tag incoming
      rfid_buffer_index = 0;
    } else if (ssvalue == 3) { // tag has been fully transmitted
      call_extract_tag = true; // extract tag at the end of the function call
    }
    if (rfid_buffer_index >= RFID_BUFFER_SIZE) { // checking for a buffer overflow (It's very unlikely that an buffer overflow comes up!)
      return;
    }

    rfid_buffer[rfid_buffer_index++] = ssvalue; // everything is alright => copy current value to buffer
    if (call_extract_tag == true) {
      if (rfid_buffer_index == RFID_BUFFER_SIZE) {
        unsigned tag = extract_tag();
        pushTag(tag);
      } else { // something is wrong... start again looking for preamble (value: 2)
        rfid_buffer_index = 0;
        return;
      }
    }
  }
}

void loop() {
  if (playing) {
    checkSensors();
  } else {
    blinkLaser();
  }

  checkRFID();
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
      blinkingLaser = -1;
    } else if (category == PROTOCOL_LASER_ON) {
      int bitmask = receivedDocument[PROTOCOL_LASER_ON_BITMASK];
      int currentBit = 1;

      for (int i = 0 ; i < N_LASERS ; i++) {
        isLaserOn[i] = (bitmask & currentBit) == currentBit;
        currentBit = currentBit << 1;
      }

      playing = true;
      blinkingLaser = -1;
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
