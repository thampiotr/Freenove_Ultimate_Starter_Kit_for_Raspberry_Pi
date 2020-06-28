/**********************************************************************
* Filename    : BreathingLED.c
* Description : Make breathing LED with PWM
* Author      : www.freenove.com
* modification: 2019/12/27
**********************************************************************/
#include <wiringPi.h>
#include <stdio.h>
#include <softPwm.h>

#define ledPin    1 

int main(void)
{
	int i;
	
	printf("Program is starting ... \n");
	
	wiringPiSetup();	//Initialize wiringPi.

    pinMode(ledPin, PWM_OUTPUT);

	pwmSetRange(100);
	pwmSetClock(500);

//	softPwmCreate(ledPin,  0, 100);//Creat SoftPWM pin
//
	while(1){
		for(i=0;i<100;i++){  //make the led brighter
			pwmWrite(ledPin, i);
			delay(10);
		}
		for(i=100;i>=0;i--){  //make the led darker
			pwmWrite(ledPin, i);
			delay(10);
		}
	}
    return 0;
}

