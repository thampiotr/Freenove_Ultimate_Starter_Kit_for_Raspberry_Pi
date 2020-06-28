#include <wiringPi.h>
#include <stdio.h>
#include <softPwm.h>

#define servoPin    1
#define CLOCK_DIV   1024*1

int main(void)
{
	int i;

	printf("Program is starting ... \n");

	wiringPiSetup();	//Initialize wiringPi.

    pinMode(servoPin, PWM_OUTPUT);

    pwmSetMode(PWM_MODE_BAL);
	pwmSetClock(CLOCK_DIV);
	pwmSetRange(100);
    printf("Clock set to %d. \n", CLOCK_DIV);


	while(1){
        printf("Writing 5 = 0 deg... \n");
		pwmWrite(servoPin, 5);
        delay(1000);
        printf("Writing 10 = 180 deg... \n");
        pwmWrite(servoPin, 10);
        delay(1000);
	}
    return 0;
}

