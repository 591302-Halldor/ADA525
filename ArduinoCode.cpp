#include <Arduino.h>
#include <AccelStepper.h>
#include <Servo.h>

AccelStepper stepper(AccelStepper::DRIVER, 7, 6);
Servo servoY;



const float scalingFactorX = 10.0;
const float scalingFactorY = 10.0;
void setup() {
  Serial.begin(115200);
  servoY.attach(9); 
  servoY.write(90);
  delay(1000); 

  stepper.setMaxSpeed(500);
  stepper.setAcceleration(250);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int xIndex = data.indexOf('X');
    int yIndex = data.indexOf('Y');
    
    if (xIndex != -1 && yIndex != -1) {
      long distanceX = data.substring(xIndex + 1, yIndex).toInt();
      long distanceY = data.substring(yIndex + 1).toInt();

      
      distanceX = -distanceX / scalingFactorX;
      distanceY = -distanceY / scalingFactorY;

      stepper.moveTo(stepper.currentPosition() + distanceX);

      
      int angleY = map(distanceY, -100, 100, 0, 180);
      servoY.write(angleY);
    }
  }

  if (stepper.distanceToGo() != 0) {
    stepper.run();
  }
}


