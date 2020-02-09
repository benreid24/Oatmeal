#ifndef SCREEN_H
#define SCREEN_H

#include <Adafruit_SSD1351.h>
#include <Adafruit_GFX.h>

class Screen {
public:
  Screen();

  void init();

  void updateReading(unsigned int i, float temp, float humid);

private:
  Adafruit_SSD1351 screen;
  char temp[2][32];
  char humid[2][32];
  int angle[2];
};

#endif
