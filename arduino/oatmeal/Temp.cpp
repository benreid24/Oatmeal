#include "Temp.h"

Temp::Temp(int pin) : sensor(pin, DHT22) {}

void Temp::init() {
  sensor.begin();
}

float Temp::readTemp() {
  return sensor.readTemperature() * 1.8 + 32;
}

float Temp::readHumidity() {
  return sensor.readHumidity();
}
