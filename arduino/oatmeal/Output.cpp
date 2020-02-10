#include <Arduino.h>
#include "Output.h"

namespace {
void printFloat(char* buf, float f) {
  const unsigned int i = f * 100;
  const unsigned int whole = i / 100;
  const unsigned int decimal = i % 100;
  sprintf(buf, "%d.%d", whole, decimal);
}
}

void Output::init() {
  Serial1.begin(115200);
}

void Output::send(const char* id, int n, float value) {
  if (!Serial1) {
    Serial.println("Serial1 not ready, skipping output");
    return;
  }
  
  char fbuf[16];
  printFloat(fbuf, value);

  char buf[128];
  sprintf(buf, "f i %s %d %s", id, n, fbuf);
  Serial1.println(buf);
}

void Output::send(const char* id, float value) {
  if (!Serial1) {
    Serial.println("Serial1 not ready, skipping output");
    return;
  }
  
  char fbuf[16];
  printFloat(fbuf, value);

  char buf[128];
  sprintf(buf, "f n %s %s", id, fbuf);
  Serial1.println(buf);
}

void Output::send(const char* id, const char* value) {
  if (!Serial1) {
    Serial.println("Serial1 not ready, skipping output");
    return;
  }
  
  char buf[128];
  sprintf(buf, "s n %s %s", id, value);
  Serial1.println(buf);
}
