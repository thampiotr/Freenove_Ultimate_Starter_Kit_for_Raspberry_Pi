#!/usr/bin/env python3
########################################################################
# Filename    : ButtonLED.py
# Description : Control led with button.
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
from gpiozero import LED, Button
from signal import pause
import time

print('Program is starting ... ')

led = LED(17)  # define LED pin according to BCM Numbering
button = Button(18)  # define Button pin according to BCM Numbering


def on_button_pressed():
    led.toggle()
    print("toggled")


def on_button_released():
    pass


button.when_pressed = on_button_pressed
button.when_released = on_button_released

pause()
