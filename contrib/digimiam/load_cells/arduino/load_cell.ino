#include <HX711-multi.h>

#define N_SCALES 2

#define HX711_CLK 2
byte HX711_DOUT_PINS[N_SCALES] = {3, 4};
long int hx711Measures[N_SCALES];
HX711MULTI hx711Scales(N_SCALES, HX711_DOUT_PINS, HX711_CLK);
float THRESHOLDS[N_SCALES] = {1, 1};
int CALIBRATIONS[N_SCALES] = {30000, 30000};

byte OUTPUT_PINS[N_SCALES] = {5, 6};

#define TARE_PIN 11
bool isTarePinActivated = true;
bool wasTarePinActivated = false;

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

    for (int i = 0 ; i < N_SCALES ; i++) {
        pinMode(OUTPUT_PINS[i], OUTPUT);
    }

    pinMode(TARE_PIN, INPUT);

    Serial.begin(9600);

    delay(100);
}

void loop() {
    hx711Scales.read(hx711Measures);
    for (int i = 0 ; i < hx711Scales.get_count() ; i++) {
        Serial.print("Scale index=");
        Serial.print(i);
        Serial.print(" [");
        if (hx711Measures[i] / CALIBRATIONS[i] >= THRESHOLDS[i]) {
            Serial.print("HIGH");
            digitalWrite(OUTPUT_PINS[i], HIGH);
        } else {
            Serial.print("LOW");
            digitalWrite(OUTPUT_PINS[i], LOW);
        }
        Serial.print("] (");
        Serial.print(hx711Measures[i] / CALIBRATIONS[i]);
        Serial.println(")");
    }
    Serial.println();

    // Rising edge manual handling
    isTarePinActivated = digitalRead(TARE_PIN);
    if (isTarePinActivated && !wasTarePinActivated) {
        hx711_tare();
    }
    wasTarePinActivated = isTarePinActivated;
}
