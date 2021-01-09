#!/usr/bin/env python3
########################################################################
# Filename    : BreathingLED.py
# Description : Breathing LED
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time

LedPin = 12  # define the LedPin

global p


def setup():
    global p
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(LedPin, GPIO.OUT)  # set LedPin to OUTPUT mode
    GPIO.output(LedPin, GPIO.LOW)  # make ledPin output LOW level to turn off LED 

    p = GPIO.PWM(LedPin, 500)  # set PWM Frequency to 500Hz
    p.start(0)  # set initial Duty Cycle to 0


sleep_seconds = 0.05


def loop():
    while True:
        for dc in range(0, 100):  # make the led brighter
            p.ChangeDutyCycle(dc)  # set dc value as the duty cycle
            time.sleep(sleep_seconds)
        for dc in reversed(range(0, 100)):  # make the led darker
            p.ChangeDutyCycle(dc)  # set dc value as the duty cycle
            time.sleep(sleep_seconds)


def destroy():
    p.stop()  # stop PWM
    GPIO.cleanup()  # Release all GPIO


if __name__ == '__main__':  # Program entrance
    print('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
