#ifndef CONTROLLER_H
#define CONTROLLER_H

#include "Pi.h"

class Controller {
public:
  Controller();

  void init();

  void handleCommand(const Pi::Command& cmd);

  void update();

private:
  bool misting;
  unsigned long long mistStartTime;
  unsigned int mistLen;
};

#endif
