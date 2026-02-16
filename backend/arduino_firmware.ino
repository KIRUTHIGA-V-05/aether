#include <Servo.h>

Servo base;
Servo arm1;
Servo arm2;
Servo gripper;

void setup() {
  Serial.begin(9600);
  base.attach(9);
  arm1.attach(10);
  arm2.attach(11);
  gripper.attach(6);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command.startsWith("G1")) {
      processG1(command);
    }
  }
}

void processG1(String cmd) {
  Serial.println("OK");
}
