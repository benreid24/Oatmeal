#ifndef OUTPUT_H
#define OUTPUT_H

class Pi {
public:
  Pi();

  void init();

  struct Command {
    enum Type {
      None,
      HeatOn,
      HeatOff,
      LightOn,
      LightOff,
      Mist
    }type;
    int param;
  };

  void send(const char* id, int n, float value);
  void send(const char* id, float value);
  void send(const char* id, const char* msg);

  Command poll();

private:
  char buf[64];

  bool append(char c);  
};

#endif
