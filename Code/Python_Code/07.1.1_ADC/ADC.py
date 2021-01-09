#!/usr/bin/env python3
########################################################################
# Filename    : ADC.py
# Description : Use ADC module to read the voltage value of potentiometer.
# Author      : www.freenove.com
# modification: 2020/03/06
########################################################################
import time

import smbus
import RPi.GPIO as GPIO

LedPin = 11  # define the LedPin


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
global p


def setup():
    global adc
    adc = PCF8591()

    global p
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(LedPin, GPIO.OUT)  # set LedPin to OUTPUT mode
    GPIO.output(LedPin, GPIO.LOW)  # make ledPin output LOW level to turn off LED

    p = GPIO.PWM(LedPin, 1000)  # set PWM Frequency to 500Hz
    p.start(0)  # set initial Duty Cycle to 0


def loop():
    while True:
        value = adc.analogRead(0)  # read the ADC value of channel 0
        voltage = value / 255.0 * 3.3  # calculate the voltage value
        percent = value / 255.0 * 100
        print('ADC Value : %d, Voltage : %.2f (%.2f%%)' % (value, voltage, percent), end="\r")
        p.ChangeDutyCycle(percent)
        time.sleep(0.1)


def destroy():
    adc.close()


if __name__ == '__main__':  # Program entrance
    print('Program is starting ... ')
    try:
        setup()
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
