#include "Temp.h"
#include "Screen.h"
#include "Motion.h"

Temp temp[] = {Temp(A0), Temp(A2)};
const size_t n = sizeof(temp) / sizeof(temp[0]);

Screen screen;

unsigned int lastRender = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("I am working");
  delay(500);

  for (unsigned int i = 0; i<n; ++i) {
    temp[i].init();
  }
  screen.init();
}

void loop() {
  Serial.println(Motion::moved());

  if (millis() - lastRender >= 2000) {
    lastRender = millis();
    for (unsigned int i = 0; i<n; ++i) {
      screen.updateReading(i, temp[i].readTemp(), temp[i].readHumidity());
    }
  }
    
  delay(200);
}
