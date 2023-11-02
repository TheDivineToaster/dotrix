#include <Servo.h>

/* --- SERVO VARIABLES --- */
Servo col1; const int col1Pin = 5;  //columns go left to right when viewing from front
Servo col2; const int col2Pin = 6;
Servo col3; const int col3Pin = 7;
Servo col4; const int col4Pin = 8;
Servo col5; const int col5Pin = 9;
Servo col6; const int col6Pin = 10;
Servo col7; const int col7Pin = 11;
Servo servos[7] = { col1, col2, col3, col4, col5, col6, col7 };

/* --- OTHER VARIABLES --- */
int closedPosition = 90;  //angle of servo when no pixels may pass
int openPosition = 0;     //angle of servo when pixel should pass
int timeOpen = 400;      //time spent open, calibrated to only allow one pixel to pass


void setup() {
  Serial.begin(9600);
  ServoWrite();
  delay(9000);
}

void loop() {
  //analyze image and decide which pixels to place

  /*for (int index = 0; index < sizeof(servos); index++) {
    Serial.println(index);
    Servo servo[] = {servos[index]};
    PlacePixel(servo);
  }
  */
  PlacePixel(servos);
  delay(2500);
  
}
/* allow one pixel to pass for each servo specified, then close all servos */
void PlacePixel(Servo servo[]) {
  for (int index = 0; index < sizeof(servo); index++) {
    servo[index].write(openPosition);
  }
  delay(timeOpen);
  for (int index = 0; index < sizeof(servo); index++) {
    servo[index].write(closedPosition);
  }
}
/* --- Setup Code, used to reduce the size of the setup function --- */
void ServoWrite() {
  Serial.println("Entered Servo Setup");
  col1.attach(col1Pin);
  col2.attach(col2Pin);
  col3.attach(col3Pin);
  col4.attach(col4Pin);
  col5.attach(col5Pin);
  col6.attach(col6Pin);
  col7.attach(col7Pin);

  for (int index = 0; index < sizeof(servos); index++) {
    servos[index].write(closedPosition);
  }
  Serial.println("Finished Servo Setup");
}
