#!/usr/bin/env python3
#############################################################################
# Filename    : Joystick.py
# Description : Read Joystick state
# Author      : www.freenove.com
# modification: 2020/03/09
########################################################################
import RPi.GPIO as GPIO
import time
import smbus

Z_Pin = 12  # define Z_Pin


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

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Z_Pin, GPIO.IN, GPIO.PUD_UP)  # set Z_Pin to pull-up mode


def draw_chart(x, y, z):
    w = 80
    h = 30

    out = ""

    px = int(w * x)
    py = int(h * y)

    for h in range(h + 1):
        out += "\n"

    out += "|"
    for x in range(w + 1):
        out += "-"
    out += "|\n"

    for y in range(h + 1):
        out += "|"
        for x in range(w + 1):
            if x == px and y == py:
                if z == 1:
                    out += "O"
                else:
                    out += "X"
            else:
                out += " "
        out += "|\n"

    out += "|"
    for x in range(w + 1):
        out += "-"
    out += "|\n"

    print(out)


def loop():
    while True:
        val_Z = GPIO.input(Z_Pin)  # read digital value of axis Z
        val_Y = adc.analogRead(0)  # read analog value of axis X and Y
        val_X = adc.analogRead(1)
        # print('value_X: %d ,\tvlue_Y: %d ,\tvalue_Z: %d' % (val_X, val_Y, val_Z))
        draw_chart(val_X / 255.0, val_Y / 255.0, val_Z)
        time.sleep(0.1)


def destroy():
    adc.close()
    GPIO.cleanup()


if __name__ == '__main__':
    print('Program is starting ... ')  # Program entrance
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
