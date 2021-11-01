#include <ArduinoJson.h>
#include <DynamixelShield.h>
#include <SoftwareSerial.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_ERROR "e"

#define PROTOCOL_PING "p"
#define PROTOCOL_REBOOT "r"
#define PROTOCOL_MOVE "m"
#define PROTOCOL_DXL_ID "i"
#define PROTOCOL_GET_POSITION "gp"
#define PROTOCOL_SET_PROFILE_VELOCITY "spv"
#define PROTOCOL_VELOCITY "v"
#define PROTOCOL_VALUE "val"
#define PROTOCOL_TORQUE_OFF "toff"
#define PROTOCOL_TORQUE_ON "ton"
#define PROTOCOL_LAST_LIB_ERR_CODE "llec"

SoftwareSerial mainSerial(10, 11);
DynamixelShield dxl;

const float DXL_PROTOCOL_VERSION = 2.0;
using namespace ControlTableItem;

#define N_DXL 1
byte dxlIds[N_DXL] = {0};

DynamicJsonDocument receivedDocument(JSON_OBJECT_SIZE(20));
String receivedEvent = "";

void setup() {
  mainSerial.begin(9600);
  dxl.begin(9600);

  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  delay(100);

  for (int i = 0 ; i < N_DXL ; i++) {
    dxl.torqueOff(dxlIds[i]);
    dxl.setOperatingMode(dxlIds[i], OP_POSITION);
    dxl.writeControlTableItem(PROFILE_VELOCITY, dxlIds[i], 25);
    dxl.torqueOn(dxlIds[i]);
    delay(100);
  }
}

void ping(int dxlId) {
    uint8_t ret = dxl.ping(dxlIds[dxlId]);

    StaticJsonDocument<JSON_OBJECT_SIZE(4)> responseEvent;
    responseEvent[PROTOCOL_CATEGORY] = PROTOCOL_PING;
    responseEvent[PROTOCOL_DXL_ID] = dxlId;
    responseEvent[PROTOCOL_VALUE] = ret;
    responseEvent[PROTOCOL_LAST_LIB_ERR_CODE] = dxl.getLastLibErrCode();

    serializeJson(responseEvent, mainSerial);
    mainSerial.println();
}

void reboot(int dxlId) {
  bool ret = dxl.reboot(dxlIds[dxlId], 100);

  StaticJsonDocument<JSON_OBJECT_SIZE(4)> responseEvent;
  responseEvent[PROTOCOL_CATEGORY] = PROTOCOL_REBOOT;
  responseEvent[PROTOCOL_DXL_ID] = dxlId;
  responseEvent[PROTOCOL_VALUE] = ret;  // Reboot succeeded if ret is true, it failed otherwise
  responseEvent[PROTOCOL_LAST_LIB_ERR_CODE] = dxl.getLastLibErrCode();

  serializeJson(responseEvent, mainSerial);
  mainSerial.println();
}

void move(int dxlId, int position) {
    dxl.setGoalPosition(dxlIds[dxlId], position);

    StaticJsonDocument<JSON_OBJECT_SIZE(4)> responseEvent;
    responseEvent[PROTOCOL_CATEGORY] = PROTOCOL_MOVE;
    responseEvent[PROTOCOL_DXL_ID] = dxlId;
    responseEvent[PROTOCOL_VALUE] = position;
    responseEvent[PROTOCOL_LAST_LIB_ERR_CODE] = dxl.getLastLibErrCode();

    serializeJson(responseEvent, mainSerial);
    mainSerial.println();
}

void getPosition(int dxlId) {
    int position = dxl.getPresentPosition(dxlIds[dxlId]);

    StaticJsonDocument<JSON_OBJECT_SIZE(4)> responseEvent;
    responseEvent[PROTOCOL_CATEGORY] = PROTOCOL_GET_POSITION;
    responseEvent[PROTOCOL_DXL_ID] = dxlId;
    responseEvent[PROTOCOL_VALUE] = position;
    responseEvent[PROTOCOL_LAST_LIB_ERR_CODE] = dxl.getLastLibErrCode();

    serializeJson(responseEvent, mainSerial);
    mainSerial.println();
}

void setVelocity(int dxlId, int velocity) {
    dxl.writeControlTableItem(MOVING_SPEED, dxlIds[dxlId], velocity);

    StaticJsonDocument<JSON_OBJECT_SIZE(4)> responseEvent;
    responseEvent[PROTOCOL_CATEGORY] = PROTOCOL_SET_PROFILE_VELOCITY;
    responseEvent[PROTOCOL_DXL_ID] = dxlId;
    responseEvent[PROTOCOL_VALUE] = velocity;
    responseEvent[PROTOCOL_LAST_LIB_ERR_CODE] = dxl.getLastLibErrCode();

    serializeJson(responseEvent, mainSerial);
    mainSerial.println();
}

void torqueOff(int dxlId) {
    dxl.torqueOff(dxlIds[dxlId]);

    StaticJsonDocument<JSON_OBJECT_SIZE(3)> responseEvent;
    responseEvent[PROTOCOL_CATEGORY] = PROTOCOL_TORQUE_OFF;
    responseEvent[PROTOCOL_DXL_ID] = dxlId;
    responseEvent[PROTOCOL_LAST_LIB_ERR_CODE] = dxl.getLastLibErrCode();

    serializeJson(responseEvent, mainSerial);
    mainSerial.println();
}

void torqueOn(int dxlId) {
    dxl.torqueOn(dxlIds[dxlId]);

    StaticJsonDocument<JSON_OBJECT_SIZE(3)> responseEvent;
    responseEvent[PROTOCOL_CATEGORY] = PROTOCOL_TORQUE_ON;
    responseEvent[PROTOCOL_DXL_ID] = dxlId;
    responseEvent[PROTOCOL_LAST_LIB_ERR_CODE] = dxl.getLastLibErrCode();

    serializeJson(responseEvent, mainSerial);
    mainSerial.println();
}

void onEvent() {
  DeserializationError error = deserializeJson(receivedDocument, receivedEvent);
  if (error != DeserializationError::Ok) {
    StaticJsonDocument<JSON_OBJECT_SIZE(2)> errorEvent;

    errorEvent[PROTOCOL_CATEGORY] = PROTOCOL_ERROR;
    errorEvent[PROTOCOL_ERROR] = error.c_str();

    serializeJson(errorEvent, mainSerial);
    Serial.println();
  } else {
    String category = receivedDocument[PROTOCOL_CATEGORY];

    int dxlId = receivedDocument[PROTOCOL_DXL_ID];

    if (category == PROTOCOL_PING) {
      ping(dxlId);
    } else if (category == PROTOCOL_REBOOT) {
      reboot(dxlId);
    } else if (category == PROTOCOL_MOVE) {
      int position = receivedDocument[PROTOCOL_VALUE];
      move(dxlId, position);
    } else if (category == PROTOCOL_GET_POSITION) {
      getPosition(dxlId);
    } else if (category == PROTOCOL_SET_PROFILE_VELOCITY) {
      int velocity = receivedDocument[PROTOCOL_VELOCITY];
      setVelocity(dxlId, velocity);
    } else if (category == PROTOCOL_TORQUE_OFF) {
      torqueOff(dxlId);
    } else if (category == PROTOCOL_TORQUE_ON) {
      torqueOn(dxlId);
    }
  }
}

void loop() {
  while (mainSerial.available()) {
    char inChar = (char)
    mainSerial.read();

    if (inChar == '\n') {
      onEvent();
      receivedEvent = "";
    } else {
      receivedEvent += inChar;
    }
  }
}