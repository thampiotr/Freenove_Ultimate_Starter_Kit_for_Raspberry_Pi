#!/usr/bin/env python3
########################################################################
# Filename    : Doorbell.py
# Description : Make doorbell with buzzer and button
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import time

from gpiozero import LED, Button
from signal import pause

print('Program is starting...')

buzzer = LED(17)
button = Button(18)

long = 300
short = long / 5

short_pause = long * 2
long_pause = 2 * short_pause
long_long_pause = 2 * short_pause

morse_map = {
    "a": [short, long],
    "b": [long, short, short, short],
    "c": [long, short, long, short],
    "d": [long, short, short],
    # "a": [long, short],
    # "a": [long, short],
    # "a": [long, short],
    # "a": [long, short],
}


def sleep_ms(ms):
    time.sleep(ms / 1000)


def say_in_morse(text):
    for c in text:
        if c in morse_map:
            for signal in morse_map[c]:
                buzzer.on()
                sleep_ms(signal)
                buzzer.off()
                sleep_ms(short_pause)
        if c == " ":
            sleep_ms(long_long_pause)
        sleep_ms(long_pause)


def onButtonPressed():
    buzzer.on()
    print("Button is pressed, buzzer turned on >>>")


def onButtonReleased():
    buzzer.off()
    print("Button is released, buzzer turned off <<<")


say_in_morse("abcd")

# button.when_pressed = onButtonPressed
# button.when_released = onButtonReleased

# pause()
