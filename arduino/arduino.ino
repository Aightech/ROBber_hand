#include <Servo.h>

Servo myservo;
unsigned char val[5]={0,0,0,0,0};
char buff[100];
char b;
void setup() {
  // initialize serial communications at 9600 bps:
  myservo.attach(9);
  Serial.begin(9600);
  val[4]='\0';
}

void loop() {
  while (Serial.available() > 0) 
  {
    if(Serial.read()=='#' && Serial.read()=='#')
    {
      for(int i =0; i<4; i++)
        val[i] = Serial.read();
      for(int i =0; i<5; i++)
        Serial.write(val[i]);
      myservo.write(val[0]);                  // sets the servo position according to the scaled value
      delay(15);
    }
  }
}
