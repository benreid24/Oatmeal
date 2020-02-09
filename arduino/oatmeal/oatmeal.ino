#include "Temp.h"
#include "Screen.h"
#include "Motion.h"
#include "Output.h"

Temp temp[] = {Temp(A0), Temp(A2)};
const size_t n = sizeof(temp) / sizeof(temp[0]);

Screen screen;

unsigned int lastRender = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("I am working");

  for (unsigned int i = 0; i<n; ++i) {
    temp[i].init();
  }
  screen.init();
  Output::init();
}

void loop() {
  if (Motion::moved()) {
    Output::send("moved", 1);
    Serial.println("Motion detected");
  }

  if (millis() - lastRender >= 2000) {
    lastRender = millis();
    for (unsigned int i = 0; i<n; ++i) {
      const float t = temp[i].readTemp();
      const float h = temp[i].readHumidity();
      screen.updateReading(i, t, h);
      Output::send("temp", i, t);
      Output::send("humid", i, h);
    }
  }
    
  delay(200);
}
