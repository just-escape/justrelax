#define CHANNELS 6

unsigned long currentTime;
unsigned long deltaTime;
unsigned long deltaTimeModulus1000;
unsigned long lastCycleStart;

// White, Purple, Red, Green, Blue, Orange
int lightPins[CHANNELS][3] = {{2, -1, -1}, {-1, -1, -1}, {-1, -1, -1}, {-1, -1, -1}, {-1, -1, -1}, {-1, -1, -1}};
int brightnesses[CHANNELS][3] = {{30, 0, 0}, {300, 0, 0}, {300, 0, 0}, {300, 0, 0}, {0, 120, 300}, {600, 72, 0}};
byte isOnPin[CHANNELS] = {48, 52, 46, 50, 42, 44};
bool isHigh[CHANNELS][3] = {{false}};

void setup() {
  for (byte i = 0 ; i < CHANNELS ; i++) {
    pinMode(isOnPin[i], INPUT);
    for (byte j = 0 ; j < 3 ; j++) {
      if (lightPins[i][j] != -1) {
        pinMode(lightPins[i][j], OUTPUT);
      }
    }
  }

  lastCycleStart = micros();
}

void loop() {
  currentTime = micros();
  deltaTime = currentTime - lastCycleStart;

  if (deltaTime > 1000) {
    lastCycleStart = currentTime;

    for (byte i = 0 ; i < CHANNELS ; i++) {
      for (byte j = 0 ; j < 3 ; j++) {
        if (lightPins[i][j] != -1) {
          isHigh[i][j] = digitalRead(qqch);
        }
      }
    }
  }

  deltaTimeModulus1000 = deltaTime % 1000;

  for (byte i = 0 ; i < CHANNELS ; i++) {
    for (byte j = 0 ; j < 3 ; j++) {
      if (lightPins[i][j] != -1) {
        if (deltaTimeModulus1000 > brightnesses[i][j]) {
          isHigh[i][j] = false;
        }
        digitalWrite(lightPins[i][j], isHigh[i][j]);
      }
    }
  }
}
