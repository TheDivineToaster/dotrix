#include <Servo.h>

/* --- SERVO VARIABLES --- */
const int numServos = 7;
Servo col1; const int col1Pin = 5;  //columns go left to right when viewing from front
Servo col2; const int col2Pin = 6;
Servo col3; const int col3Pin = 7;
Servo col4; const int col4Pin = 8;
Servo col5; const int col5Pin = 9;
Servo col6; const int col6Pin = 10;
Servo col7; const int col7Pin = 11;
Servo servos[numServos] = { col1, col2, col3, col4, col5, col6, col7 };
int blockCol[numServos];
int blockIndex = 0;

/* --- GATE VARIABLES --- */
const int closedPosition = 90;  //angle of servo when no pixels may pass
const int openPosition = 0;     //angle of servo when pixel should pass
const int timeOpen = 400;      //time spent open, calibrated to only allow one pixel to pass
const int timeBetweenRows = 2500; //replace with limit switch eventually

/* --- SETUP FUNCTION --- */
void setup() {
  Serial.begin(9600);
  ServoWrite();
}
/* --- LOOP FUNCTION --- */
void loop() {
  //analyze image and decide which columns to block, then call PlacePixel
  /*blockIndex = 0;
  for (int i = 0; i < number of columns blocking; i++) {
    blockCol[i] = column index
    blockIndex++;
  }*/

  PlacePixel();
  delay(timeBetweenRows);
  
}

/* allow one pixel to pass for each servo specified, then close all servos */
void PlacePixel() {
  Serial.print("Releasing row. Blocking columns: ");
  for (int i = 0; i < blockIndex; i++) {
    servos[blockCol[i]].write(openPosition);
  }
  delay(timeOpen);
  for (int i = 0; i < blockIndex; i++) {
    servos[blockCol[i]].write(closedPosition);
  }
}

/* --- HELPER FUNCTIONS --- */

// Setup Code, used to reduce the size of the setup function
void ServoWrite() {
  Serial.println("Entered Servo Setup");
  col1.attach(col1Pin);
  col2.attach(col2Pin);
  col3.attach(col3Pin);
  col4.attach(col4Pin);
  col5.attach(col5Pin);
  col6.attach(col6Pin);
  col7.attach(col7Pin);

  for (int index = 0; index < numServos; index++) {
    servos[index].write(closedPosition);
  }
  Serial.println("Finished Servo Setup and initialized all to neutral position");
}
