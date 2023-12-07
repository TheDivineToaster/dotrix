/* Pin Names and Numbers */
const int horizPot = A0;
const int vertPot = A2;
const int speedPot = A4;


char data[15] = {0};
char horiz[25] = {0};
char vert[25] = {0};
char speed[25] = {0};

void setup() {
  Serial.begin(9600);           //Starting serial communication

  pinMode(horizPot, INPUT);
  pinMode(vertPot, INPUT);
  pinMode(speedPot, INPUT);
  
}
  
void loop() {
  int horizVal = analogRead(horizPot);
  int vertVal = analogRead(vertPot);
  int speedVal = analogRead(speedPot);

  itoa(horizVal, data, 10);
  strcpy(horiz, "Horiz: ");
  strcat(horiz, data);
  Serial.println(horiz);

  itoa(vertVal, data, 10);
  strcpy(vert, "Vert: ");
  strcat(vert, data);
  Serial.println(vert);

  itoa(speedVal, data, 10);
  strcpy(speed, "Speed: ");
  strcat(speed, data);
  Serial.println(speed);
}
