#include <DHT.h>
#include "Screen.h"

DHT dht1 = DHT(A0, DHT22);
Screen screen;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("I am working");
  delay(500);
  dht1.begin();
  screen.init();
}

void loop() {
  const float f = dht1.readTemperature() * 1.8 + 32;
  const float h = dht1.readHumidity();
  
  Serial.print(f);
  Serial.print("F ");
  Serial.print(h);
  Serial.println("%");

  screen.updateReading(0, f, h);
  screen.updateReading(1, f-8, h-5);
    
  delay(2000);
}
