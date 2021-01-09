#!/usr/bin/env python3
#############################################################################
# Filename    : Thermometer.py
# Description : DIY Thermometer
# Author      : www.freenove.com
# modification: 2019/03/09
########################################################################
import RPi.GPIO as GPIO
import time
import math

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


global adc


def setup():
    global adc
    adc = PCF8591()


def celsius_to_kelvin(c):
    return 273.15 + c


def kelvin_to_celsius(k):
    return k - 273.15


def loop():
    while True:
        value = adc.analogRead(0)  # read ADC value A0 pin
        U_in = 3.3
        R_2 = 10_000
        B = 3950
        R_1 = 10_000
        T_1 = celsius_to_kelvin(25)

        V_t = value / 255.0 * U_in

        R_t = (R_2 * V_t) / (U_in - V_t)

        T_2 = 1 / (1 / B * math.log(R_t / R_1) + 1 / T_1)
        T_2_C = kelvin_to_celsius(T_2)

        print('ADC Value : %5.d, Voltage : %5.2f, Temperature : %5.2f' % (value, V_t, T_2_C), end="\r")
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
