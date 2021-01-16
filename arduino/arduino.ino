#include <Servo.h>
#define NB_FINGER 4

unsigned char crc;
Servo myservo[NB_FINGER];
unsigned char pos[NB_FINGER];
unsigned char limit[NB_FINGER][2] = { {0,83},
                                      {84,0},
                                      {0,83},
                                      {84,0}};

void setup() {
  // initialize servo motors
  for(int i =0; i<NB_FINGER; i++)
    myservo[i].attach(6+i);
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  while (Serial.available() > 0)//wait for data
  {
    if(Serial.read()=='#' && Serial.read()=='#')//if the two first bytes are ## then decode
    {
      crc=0;
      for(int i =0; i<NB_FINGER; i++)//read data and compute crc
        crc += pos[i] = Serial.read();
        
      if(true ||crc == Serial.read())//if crc is correct then set the servo position
        for(int i =0; i<NB_FINGER; i++)
          myservo[i].write(pos[i]/255.0f*(limit[i][1]-limit[i][0])+limit[i][0]);
      
      Serial.write(crc);//return the crc
      delay(15);
    }
  }
}
