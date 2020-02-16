#include "Temp.h"
#include "Screen.h"
#include "Motion.h"
#include "Pi.h"
#include "Controller.h"

#define RENDER_PERIOD 1500

Pi pi;
Controller controller;
Temp temp[] = {Temp(A0), Temp(A2)};
const size_t sensorCount = sizeof(temp) / sizeof(temp[0]);

Screen screen;

unsigned int lastRender = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("I am working");

  for (unsigned int i = 0; i<sensorCount; ++i) {
    temp[i].init();
  }
  screen.init();
  pi.init();
  controller.init();
}

void loop() {
  if (Motion::moved()) {
    pi.send("motion", 1);
  }

  if (millis() - lastRender >= RENDER_PERIOD) {
    lastRender = millis();
    for (unsigned int i = 0; i<sensorCount; ++i) {
      const float t = temp[i].readTemp();
      const float h = temp[i].readHumidity();
      screen.updateReading(i, t, h);
      pi.send("temp", i, t);
      pi.send("humid", i, h);
    }
  }

  Pi::Command cmd = pi.poll();
  if (cmd.type != Pi::Command::None) {
    controller.handleCommand(cmd);
    Serial.print(cmd.type);
    Serial.print(" ");
    Serial.println(cmd.param);
  }

  controller.update();
    
  delay(500);
}
