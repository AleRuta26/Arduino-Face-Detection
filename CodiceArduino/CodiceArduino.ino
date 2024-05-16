#include <Servo.h>

// C++ code
//
Servo s1;
Servo s2;
String x;
int versox = 1;
int versoy = 1;
int posx = 0;
int posy = 60;
void setup() {
  s1.attach(10);
  s2.attach(9);
  Serial.begin(460800);
}

void loop() {
  if (Serial.available()) {
    String pos = Serial.readStringUntil(',');
    posx = pos.toInt();
    posy = Serial.readStringUntil('\n').toInt();
    if (posx == -1 && posy == -1) {
      posx = s1.read();
      posy = s2.read();
      s1.write(posx + versox);
      s2.write(posy + versoy);
      if (s1.read() == 180 || s1.read() == 0) {
        versox *= -1;
      }
      if (s2.read() > 110 || s2.read() < 60) {
        versoy *= -1;
        if (s2.read() >= 110)
          s2.write(109);
        else
          s2.write(61);
      }
    } else {
      if (posx < 40) {
        s1.write(s1.read() + 1);
      } else if (posx > 60) {
        s1.write(s1.read() - 1);
      }
      if (posy < 40) {
        s2.write(s2.read() - 1);
      } else if (posy > 60) {
        s2.write(s2.read() + 1);
      }
    }
    delay(20);
  }
}