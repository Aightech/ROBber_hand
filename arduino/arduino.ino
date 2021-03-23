#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

//#define DEBUG
#define NB_FINGER 4
#define SERVOMIN  440 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  470 // This is the 'maximum' pulse length count (out of 4096)
int s_range = SERVOMAX-SERVOMIN;

unsigned char crc;
unsigned char pos[NB_FINGER] = {20, 00, 100, 00};
int limit[NB_FINGER][2] = { {400, 280},
                                      {200, 385},
                                      {320, 170},
                                      {180, 360}};

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(50);  // This is the maximum PWM frequency

   
}

void loop() {

 #ifdef DEBUG
//    for(int i =0; i<NB_FINGER; i++)
//         pwm.setPWM(i, 0, pos[i]/255.0f*(limit[i][1]-limit[i][0])+limit[i][0]);
    delay(15);
    int i = 3;
    pwm.setPWM(i, 0, 200);
  #endif
   
  
  while (Serial.available() > NB_FINGER+3)//wait for data
  {
    if(Serial.read()=='#' && Serial.read()=='#')//if the two first bytes are ## then decode
    {
      crc=0;
      for(int i =0; i<NB_FINGER; i++)//read data and compute crc
        crc += pos[i] = Serial.read();

      for(int i =0; i<NB_FINGER; i++)//read data and compute crc
        pos[i] = min(255, max(0, pos[i]));

      if( crc == Serial.read())//if crc is correct then set the servo position
      {
        for(int i =0; i<NB_FINGER; i++)
          pwm.setPWM(i, 0, pos[i]/255.0f*(limit[i][1]-limit[i][0])+limit[i][0]);
        Serial.write(1);//return the crc
      }
      else
        Serial.write(0);
         
      delay(15);
    }
  }
}
