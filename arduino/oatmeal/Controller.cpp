#include <Arduino.h>
#include "Controller.h"

#define HEAT_PIN  22
#define LIGHT_PIN 23
#define MIST_PIN  24

Controller::Controller()
: misting(false)
, mistStartTime(0)
, mistLen(0) {}

void Controller::init() {
  pinMode(HEAT_PIN, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(MIST_PIN, OUTPUT);
}

void Controller::update() {
  if (misting) {
    if (millis() - mistStartTime >= mistLen) {
      digitalWrite(MIST_PIN, LOW);
      misting = false;
      mistLen = mistStartTime = 0;
    }
  }
}

void Controller::handleCommand(const Pi::Command& cmd) {
  switch (cmd.type) {
    case Pi::Command::HeatOn:
      digitalWrite(HEAT_PIN, HIGH);
      break;
    case Pi::Command::HeatOff:
      digitalWrite(HEAT_PIN, LOW);
      break;

    case Pi::Command::LightOn:
      digitalWrite(LIGHT_PIN, HIGH);
      break;
    case Pi::Command::LightOff:
      digitalWrite(LIGHT_PIN, LOW);
      break;

    case Pi::Command::Mist:
      misting = true;
      mistLen = cmd.param;
      mistStartTime = millis();
      digitalWrite(MIST_PIN, HIGH);
      break;

    default:
      Serial.print("Unrecognized command type ");
      Serial.print(cmd.type);
      Serial.println();
      break;
  }
}
