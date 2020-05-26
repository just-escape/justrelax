#include <HX711-multi.h>

#define HX711_CLK 2
byte HX711_DOUT_PINS[2] = {3, 4};
long int hx711Measures[2];
HX711MULTI hx711Scales(2, HX711_DOUT_PINS, HX711_CLK);

byte OUTPUT_PINS[2] = {5, 6};

#define THRESHOLD 5

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

    for (int i = 0 ; i < 2 ; i++) {
        pinMode(OUTPUT_PINS[i], OUTPUT);
    }

    delay(100);
}

void loop() {
    hx711Scales.read(hx711Measures);
    for (int i = 0 ; i < hx711Scales.get_count() ; i++) {
        if (hx711Measures[i] / 40000 >= THRESHOLD) {
            digitalWrite(OUTPUT_PINS[i], HIGH);
        } else {
            digitalWrite(OUTPUT_PINS[i], LOW);
        }
    }
}
