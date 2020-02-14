#include <Arduino.h>
#include "Pi.h"

namespace {
void printFloat(char* buf, float f) {
  const unsigned int i = f * 100;
  const unsigned int whole = i / 100;
  const unsigned int decimal = i % 100;
  sprintf(buf, "%d.%d", whole, decimal);
}
}

Pi::Pi() {
  memcpy(buf, 0, sizeof(buf));
}

void Pi::init() {
  Serial1.begin(115200);
}

void Pi::send(const char* id, int n, float value) {
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

void Pi::send(const char* id, float value) {
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

void Pi::send(const char* id, const char* value) {
  if (!Serial1) {
    Serial.println("Serial1 not ready, skipping output");
    return;
  }
  
  char buf[128];
  sprintf(buf, "s n %s %s", id, value);
  Serial1.println(buf);
}

Pi::Command Pi::poll() {
  Command cmd;
  cmd.type = Command::None;
  cmd.param = 0;
  int b = Serial1.read();
  while (b != -1) {
    if (static_cast<char>(b) == '\n') {
      //TODO - parse into Command struct and return
    }
    else if (!append(b)) {
      Serial.println("Error appending to serial buffer, buffer full. Clearing");
      buf[0] = 0;
      return cmd;
    }
  }
}

bool Pi::append(char c) {
  const size_t len = strlen(buf);
  if (len >= sizeof(buf) - 1)
    return false;
  buf[len] = c;
  buf[len+1] = 0;
}
