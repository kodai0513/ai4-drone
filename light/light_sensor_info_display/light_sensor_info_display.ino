#include <M5StickCPlus2.h>

#define LIGHT_SENSOR_PIN 33 

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);
  Serial.begin(115200);
  M5.Display.println("Light Sensor Start");
}

void loop() {
  int lightValue = analogRead(LIGHT_SENSOR_PIN);
  Serial.println(lightValue);
  delay(100); 
}