#ifndef OUTPUT_H
#define OUTPUT_H

class Output {
public:
  static void init();

  static void send(const char* id, int n, float value);
  static void send(const char* id, float value);
  static void send(const char* id, const char* msg);
};

#endif
