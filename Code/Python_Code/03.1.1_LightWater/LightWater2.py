#!/usr/bin/env python3
########################################################################
# Filename    : LightWater.py
# Description : Use LEDBar Graph(10 LED) 
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import threading

from gpiozero import LEDBoard
from time import sleep
from signal import pause

print('Program is starting ... ')

ledPins = ["J8:11", "J8:12", "J8:13", "J8:15", "J8:16", "J8:18", "J8:22", "J8:3", "J8:5", "J8:24"]

leds = LEDBoard(*ledPins, active_high=False)

sleep_time = 0.05

running = True


def circulate(f, t):
    while running:
        for i in range(f, t):
            leds.on(i)
            sleep(sleep_time)
            leds.off(i)
        for i in reversed(range(f, t)):
            leds.on(i)
            sleep(sleep_time)
            leds.off(i)
    print("Done.")


def circulate_reverse(f, t):
    while running:
        for i in reversed(range(f, t)):
            leds.on(i)
            sleep(sleep_time)
            leds.off(i)
        for i in range(f, t):
            leds.on(i)
            sleep(sleep_time)
            leds.off(i)
    print("Done.")


def main():
    global running
    try:
        t0 = threading.Thread(target=circulate, args=(0, 5))
        t0.start()

        t1 = threading.Thread(target=circulate_reverse, args=(5, 10))
        t1.start()

        # t2 = threading.Thread(target=circulate, args=(4, 6))
        # t2.start()
        #
        # t3 = threading.Thread(target=circulate, args=(6, 8))
        # t3.start()
        #
        # t4 = threading.Thread(target=circulate, args=(8, 10))
        # t4.start()

        t0.join()
    except KeyboardInterrupt:
        print("Keyboard interrupted. Terminating...")
        running = False
        return


if __name__ == '__main__':
    main()

#
# while True:
#     for index in range(0, len(ledPins), 1):  # move led(on) from left to right
#         leds.on(index)
#         sleep(sleep_time)
#         leds.off(index)
#     for index in range(len(ledPins) - 1, -1, -1):  # move led(on) from right to left
#         leds.on(index)
#         sleep(sleep_time)
#         leds.off(index)
