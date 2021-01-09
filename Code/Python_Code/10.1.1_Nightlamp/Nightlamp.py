#!/usr/bin/env python3
#############################################################################
# Filename    : Nightlamp.py
# Description : Control LED with Photoresistor
# Author      : www.freenove.com
# modification: 2020/03/09
########################################################################
import RPi.GPIO as GPIO
import time

import smbus


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


ledPin = 11  # define ledPin
global adc


def setup():
    global adc
    adc = PCF8591()
    global p
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)  # set ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW)

    p = GPIO.PWM(ledPin, 1000)  # set PWM Frequence to 1kHz
    p.start(0)


low = 40
high = 80


def loop():
    while True:
        value = adc.analogRead(0)  # read the ADC value of channel 0
        value = (value - low) / (high - low) * 255
        if value < 0:
            value = 0
        if value > 255:
            value = 255
        p.ChangeDutyCycle(value * 100 / 255)
        voltage = value / 255.0 * 3.3
        print('ADC Value : %d, Voltage : %.2f' % (value, voltage))
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
