#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define NB_FINGER 4
#define SERVOMIN  440 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  470 // This is the 'maximum' pulse length count (out of 4096)
int s_range = SERVOMAX-SERVOMIN;

unsigned char crc;
unsigned char pos[NB_FINGER] = {40, 40, 40, 40};
unsigned char limit[NB_FINGER][2] = { {0,83},
                                      {84,0},
                                      {0,83},
                                      {84,0}};

void setup() {
  Serial.begin(9600);
  Serial.println("hey");

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(1600);  // This is the maximum PWM frequency
  Wire.setClock(400000);
}

void loop() {

  #ifdef DEBUG
    for(int i =0; i<NB_FINGER; i++)
         pwm.setPWM(i, 0, pos[i]/255.0f*(limit[i][1]-limit[i][0])+limit[i][0]);
    delay(15);
  #endif
  
  while (Serial.available() > 0)//wait for data
  {
    if(Serial.read()=='#' && Serial.read()=='#')//if the two first bytes are ## then decode
    {
      crc=0;
      for(int i =0; i<NB_FINGER; i++)//read data and compute crc
        crc += pos[i] = Serial.read();
        
      if(true ||crc == Serial.read())//if crc is correct then set the servo position
        for(int i =0; i<NB_FINGER; i++)
          pwm.setPWM(i, 0, pos[i]/255.0f*(limit[i][1]-limit[i][0])+limit[i][0]);
      
      Serial.write(crc);//return the crc
      delay(15);
    }
  }
}
