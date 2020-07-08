#define CHANNELS 6

unsigned long currentTime;
unsigned long deltaTime;
unsigned long deltaTimeModulus1000;
unsigned long lastCycleStart;

// White, Purple, Red, Green, Blue, Orange
int lightPins[CHANNELS][3] = {{2, -1, -1}, {3, -1, -1}, {4, -1, -1}, {5, -1, -1}, {6, 7, 8}, {9, 10, 11}};
int brightnesses[CHANNELS][3] = {{300, 0, 0}, {300, 0, 0}, {300, 0, 0}, {300, 0, 0}, {0, 120, 300}, {600, 72, 0}};
bool isOnPin[CHANNELS] = {48, 52, 46, 50, 42, 44};

void setup() {
  for (int i = 0 ; i < CHANNELS ; i++) {
    pinMode(isOnPin[i], INPUT);
    for (int j = 0 ; j < 3 ; j++) {
      if (lightPins[i][j] != -1) {
        pinMode(lightPins[i][j], OUTPUT);
      }
    }
  }

  Serial.begin(9600);
  lastCycleStart = micros();
}

void loop() {
  currentTime = micros();
  deltaTime = currentTime - lastCycleStart;

  if (deltaTime > 1000) {
    lastCycleStart = currentTime;

    for (int i = 0 ; i < CHANNELS ; i++) {
      for (int j = 0 ; j < 3 ; j++) {
        digitalWrite(lightPins[i][j], digitalRead(isOnPin[i]));
      }
    }
  }

  deltaTimeModulus1000 = deltaTime % 1000;

  for (int i = 0 ; i < CHANNELS ; i++) {
    for (int j = 0 ; j < 3 ; j++) {
      if (lightPins[i][j] != -1) {
        if (deltaTimeModulus1000 > brightnesses[i][j]) {
          digitalWrite(lightPins[i][j], false);
        }
      }
    }
  }
}