#include <HX711-multi.h>

#include <ArduinoJson.h>

#define PROTOCOL_CATEGORY "c"

#define PROTOCOL_MEASURE "m"
#define PROTOCOL_CELL_ID "i"
#define PROTOCOL_VALUE "v"

#define HX711_CLK 2
byte HX711_DOUT_PINS[2] = {3, 4};
long int hx711Measures[2];
long int lastHX711Measures[2] = {0};
HX711MULTI hx711Scales(2, HX711_DOUT_PINS, HX711_CLK);


void hx711_tare() {
    bool isTareSuccessful = false;
    unsigned long tareTimeout = 4000;

    unsigned long tareStartTime = millis();
    while (!isTareSuccessful && millis() < (tareStartTime + tareTimeout)) {
        isTareSuccessful = hx711Scales.tare(20, 10000);
    }
}

void setup() {
    Serial.begin(9600);

    hx711_tare();

    delay(100);
}

void notifyMeasure(int cellId, long int value) {
    StaticJsonDocument<JSON_OBJECT_SIZE(3)> event;

    event[PROTOCOL_CATEGORY] = PROTOCOL_MEASURE;
    event[PROTOCOL_CELL_ID] = cellId;
    event[PROTOCOL_VALUE] = value;

    serializeJson(event, Serial);
    Serial.println();
}

void loop() {
    hx711Scales.read(hx711Measures);
    for (int i = 0 ; i < hx711Scales.get_count() ; i++) {
        if (lastHX711Measures[i] != hx711Measures[i] / 40000) {
            notifyMeasure(i, hx711Measures[i] / 40000);
            lastHX711Measures[i] = hx711Measures[i] / 40000;
        }
    }
}
