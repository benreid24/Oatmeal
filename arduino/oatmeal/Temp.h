#ifndef TEMP_H
#define TEMP_H

#include <DHT.h>

class Temp {
public:
  Temp(int pin);

  void init();

  float readTemp();
  float readHumidity();

private:
  DHT sensor;
};

#endif
