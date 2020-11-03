#include "HX711.h"

#define DOUT  3
#define CLK  2
#define rpi_tx 5

HX711 scale;

float calibration_factor = -46;

void setup() {
  pinMode(rpi_tx, OUTPUT);

  Serial.begin(9600);
  Serial.println("HX711 calibration sketch");

  scale.begin(DOUT, CLK);
  scale.set_scale();
  scale.tare();

  long zero_factor = scale.read_average();
  Serial.print("Zero factor: ");
  Serial.println(zero_factor);
  Serial.print("Calibration factor: ");
  Serial.print(calibration_factor);
  Serial.println();
  scale.set_scale(calibration_factor);
}

void loop() {
  float unit = scale.get_units() * -0.001;
  Serial.print("Weight: ");
  Serial.print(unit);
  Serial.print(" kg");
  Serial.println();
}
