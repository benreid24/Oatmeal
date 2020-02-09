#include <Arduino.h>
#include "Motion.h"

bool Motion::moved() {
  return analogRead(1) > 500;
}
