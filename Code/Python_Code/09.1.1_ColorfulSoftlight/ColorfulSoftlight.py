#!/usr/bin/env python3
#############################################################################
# Filename    : Softlight.py
# Description : Control RGBLED with Potentiometer 
# Author      : www.freenove.com
# modification: 2020/03/09
########################################################################
import time

import smbus
import RPi.GPIO as GPIO

ledRedPin = 15  # define 3 pins for RGBLED
ledGreenPin = 13
ledBluePin = 11


class PCF8591:
    def __init__(self):
        self.cmd = 0x40  # The default command for PCF8591 is 0x40.
        self.address = 0x48  # 0x48 is the default i2c address for PCF8591 Module.
        self.bus = smbus.SMBus(1)

    def analogRead(self, chn):  # PCF8591 has 4 ADC input pins, chn:0,1,2,3
        value = self.bus.read_byte_data(self.address, self.cmd + chn)
        value = self.bus.read_byte_data(self.address, self.cmd + chn)
        return value

    def analogWrite(self, value):  # write DAC value
        self.bus.write_byte_data(self.address, self.cmd, value)

    def close(self):
        self.bus.close()


global adc
global p_Red, p_Green, p_Blue


def setup():
    global adc
    adc = PCF8591()

    global p_Red, p_Green, p_Blue
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledRedPin, GPIO.OUT)
    GPIO.setup(ledGreenPin, GPIO.OUT)
    GPIO.setup(ledBluePin, GPIO.OUT)

    p_Red = GPIO.PWM(ledRedPin, 1000)
    p_Red.start(0)
    p_Green = GPIO.PWM(ledGreenPin, 1000)
    p_Green.start(0)
    p_Blue = GPIO.PWM(ledBluePin, 1000)
    p_Blue.start(0)


def loop():
    while True:
        value_Red = adc.analogRead(0)  # read ADC value of 3 potentiometers
        value_Green = adc.analogRead(1)
        value_Blue = adc.analogRead(2)
        p_Red.ChangeDutyCycle(value_Red * 100 / 255)
        p_Green.ChangeDutyCycle(value_Green * 100 / 255)
        p_Blue.ChangeDutyCycle(value_Blue * 100 / 255)
        # print read ADC value
        print('ADC Value value_Red: %d ,\tvlue_Green: %d ,\tvalue_Blue: %d' % (value_Red, value_Green, value_Blue), end="\r")
        time.sleep(0.01)


def destroy():
    adc.close()
    GPIO.cleanup()


if __name__ == '__main__':  # Program entrance
    print('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
