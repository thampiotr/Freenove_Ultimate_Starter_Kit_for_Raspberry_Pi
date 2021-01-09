/**********************************************************************
* Filename    : SteppingMotor.c
* Description : Drive stepping Motor
* Author      : www.freenove.com
* modification: 2019/12/27
**********************************************************************/
#include <stdio.h>
#include <wiringPi.h>

const int motorPins[]={1,4,5,6};
int delay_ms = 3;
int cycles = 128;

int move_cycles(int cw, int cycles, int cycle_delay_ms) {
        for (int cycle=0; cycle<cycles; cycle++) {
            for (int phase=0; phase<4; phase++) {
                int actualPhase = phase;
                if (cw == 0) {
                    actualPhase = 3-phase;
                }
                for (int pin=0; pin<4; pin++) {
                    if (actualPhase == pin) {
                        digitalWrite(motorPins[pin], HIGH);
                    } else {
                        digitalWrite(motorPins[pin], LOW);
                    }
                }
                delay(cycle_delay_ms);
            }
        }
}

int main(void){
    printf("Program is starting ...\n");
    wiringPiSetup();
    for(int i=0;i<4;i++){
        pinMode(motorPins[i],OUTPUT);
    }

    while(1) {
        move_cycles(1, cycles, delay_ms);
        move_cycles(0, cycles, delay_ms);
    }
    return 0;
}

