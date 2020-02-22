#include <Arduino.h>
#include "Pi.h"

namespace {
void printFloat(char* buf, float f) {
  const unsigned int i = f * 100;
  const unsigned int whole = i / 100;
  const unsigned int decimal = i % 100;
  sprintf(buf, "%d.%d", whole, decimal);
}

auto& serial = Serial1;

}

Pi::Pi() {
  buf[0] = 0;
}

void Pi::init() {
  Serial1.begin(115200);
}

void Pi::send(const char* id, int n, float value) {
  if (!serial) {
    Serial.println("Serial1 not ready, skipping output");
    return;
  }
  
  char fbuf[16];
  printFloat(fbuf, value);

  char buf[128];
  sprintf(buf, "f i %s %d %s", id, n, fbuf);
  serial.println(buf);
}

void Pi::send(const char* id, float value) {
  if (!serial) {
    Serial.println("Serial1 not ready, skipping output");
    return;
  }
  
  char fbuf[16];
  printFloat(fbuf, value);

  char buf[128];
  sprintf(buf, "f n %s %s", id, fbuf);
  serial.println(buf);
}

void Pi::send(const char* id, const char* value) {
  if (!serial) {
    Serial.println("Serial1 not ready, skipping output");
    return;
  }
  
  char buf[128];
  sprintf(buf, "s n %s %s", id, value);
  serial.println(buf);
}

Pi::Command Pi::poll() {
  Command command;
  command.type = Command::None;
  command.param = 0;
  int b = serial.read();
  while (b != -1) {
    if (static_cast<char>(b) == '\n') {
      char cmd[16];
      unsigned int i = 0;
      for (; i<strlen(buf) && buf[i]!=' ' && i<15; ++i) {
        cmd[i] = buf[i];
      }
      cmd[i] = 0;

      if (strcmp(cmd, "heaton") == 0) command.type = Command::HeatOn;
      else if (strcmp(cmd, "heatoff") == 0) command.type = Command::HeatOff;
      else if (strcmp(cmd, "lighton") == 0) command.type = Command::LightOn;
      else if (strcmp(cmd, "lightoff") == 0) command.type = Command::LightOff;
      else if (strcmp(cmd, "mist") == 0) {
        command.type = Command::Mist;
        command.param = String(&buf[i]).toInt();
      }
      else {
        Serial.print("Unrecognized command '");
        Serial.print(cmd);
        Serial.println("'");
      }
      buf[0] = 0;
      break;
    }
    else if (!append(b)) {
      Serial.println("Error appending to serial buffer, buffer full. Clearing");
      buf[0] = 0;
    }
    b = serial.read();
  }
  return command;
}

bool Pi::append(char c) {
  const size_t len = strlen(buf);
  if (len >= sizeof(buf) - 1)
    return false;
  buf[len] = c;
  buf[len+1] = 0;
  return true;
}
