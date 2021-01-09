/**********************************************************************
* Filename    : LightWater02.c
* Description : Control LED by 74HC595
* Author      : www.freenove.com
* modification: 2019/12/27
**********************************************************************/
#include <wiringPi.h>
#include <stdio.h>
#include <wiringShift.h>

#define   dataPin   0   //DS Pin of 74HC595(Pin14)
#define   latchPin  2   //ST_CP Pin of 74HC595(Pin12)
#define   clockPin 3    //CH_CP Pin of 74HC595(Pin11)

#define WRITE_CLOCK_PERIOD_MICROSECONDS 5
#define LIGHT_SWITCH_PERIOD_MILLISECONDS 1000

void _shiftOut(int dPin,int cPin,int val){
    digitalWrite(latchPin,LOW);		// Output low level to latchPin
	int i;
    for(i = 0; i < 8; i++){
        digitalWrite(cPin,LOW);
        digitalWrite(dPin, (0x01&(val>>i)) ? HIGH : LOW);
        delayMicroseconds(WRITE_CLOCK_PERIOD_MICROSECONDS);
        digitalWrite(cPin,HIGH);
        delayMicroseconds(WRITE_CLOCK_PERIOD_MICROSECONDS);
	}
    digitalWrite(latchPin,HIGH);   //Output high level to latchPin, and 74HC595 will update the data to the parallel output port.
}

int main(void)
{
	int i;
	unsigned char x = 0;
	
	printf("Program is starting ...\n");
	
	wiringPiSetup();
	
	pinMode(dataPin,OUTPUT);
	pinMode(latchPin,OUTPUT);
	pinMode(clockPin,OUTPUT);
	while(1){
//	    // Show binary numbers :)
//        printf("X is set to: %d\n", x);
//        _shiftOut(dataPin,clockPin,x);
//		delay(LIGHT_SWITCH_PERIOD_MILLISECONDS);
//        x++;

		x=0x01;
		for(i=0;i<8;i++){
		    unsigned char newx = x >> 1;
		    if (newx == 0) newx = 0x80;
		    newx = ~newx;
		    printf("X is set to: %d\n", newx);
			_shiftOut(dataPin,clockPin,newx);// Send serial data to 74HC595
			x<<=1;      //make the variable move one bit to left once, then the bright LED move one step to the left once.
			delay(LIGHT_SWITCH_PERIOD_MILLISECONDS);
		}
		x=0x80;
		for(i=0;i<8;i++){
		    unsigned char newx = x >> 1;
		    if (newx == 0) newx = 0x80;
		    newx = ~newx;
		    printf("X is set to: %d\n", newx);
			_shiftOut(dataPin,clockPin,newx);// Send serial data to 74HC595
			x>>=1;
			delay(LIGHT_SWITCH_PERIOD_MILLISECONDS);
		}
	}
	return 0;
}

