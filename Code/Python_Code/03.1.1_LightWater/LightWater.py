#!/usr/bin/env python3
########################################################################
# Filename    : LightWater.py
# Description : Use LEDBar Graph(10 LED) 
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time

ledPins = [11, 12, 13, 15, 16, 18, 22, 3, 5, 24, 26]


def setup():
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPins, GPIO.OUT)  # set all ledPins to OUTPUT mode
    GPIO.output(ledPins, GPIO.HIGH)  # make all ledPins output HIGH level, turn off all led


sleep_seconds = 0.5


def loop():
    while True:
        for pin in ledPins:  # make led(on) move from left to right
            GPIO.output(pin, GPIO.LOW)
            time.sleep(sleep_seconds)
            GPIO.output(pin, GPIO.HIGH)
        for pin in ledPins[::-1]:  # make led(on) move from right to left
            GPIO.output(pin, GPIO.LOW)
            time.sleep(sleep_seconds)
            GPIO.output(pin, GPIO.HIGH)


def destroy():
    GPIO.cleanup()  # Release all GPIO


if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    setup()
    try:
        GPIO.output(5, GPIO.LOW)
        time.sleep(1)
        GPIO.output(26, GPIO.LOW)
        time.sleep(1)
        GPIO.output(24, GPIO.LOW)
        time.sleep(1)
        destroy()
        # loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
