#include <HX711-multi.h>

#define HX711_CLK 2
byte HX711_DOUT_PINS[1] = {3};
long int hx711Measures[1];
HX711MULTI hx711Scales(1, HX711_DOUT_PINS, HX711_CLK);

byte OUTPUT_PINS[1] = {5};

#define TARE_PIN 11
bool isTarePinActivated = true;
bool wasTarePinActivated = false;

#define THRESHOLD 1

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

    for (int i = 0 ; i < 1 ; i++) {
        pinMode(OUTPUT_PINS[i], OUTPUT);
    }

    pinMode(TARE_PIN, INPUT);

    delay(100);
}

void loop() {
    hx711Scales.read(hx711Measures);
    for (int i = 0 ; i < hx711Scales.get_count() ; i++) {
        if (hx711Measures[i] / 30000 >= THRESHOLD) {
            digitalWrite(OUTPUT_PINS[i], HIGH);
        } else {
            digitalWrite(OUTPUT_PINS[i], LOW);
        }
    }

    // Rising edge manual handling
    isTarePinActivated = digitalRead(TARE_PIN);
    if (isTarePinActivated && !wasTarePinActivated) {
        hx711_tare();
    }
    wasTarePinActivated = isTarePinActivated;
}
