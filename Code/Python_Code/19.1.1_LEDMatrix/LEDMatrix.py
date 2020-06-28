#!/usr/bin/env python3
#############################################################################
# Filename    : LEDMatrix.py
# Description : Control LEDMatrix with 74HC595
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import math

import RPi.GPIO as GPIO
import time

# define the pins connect to 74HC595
dataPin = 11  # DS Pin of 74HC595(Pin14)
latchPin = 13  # ST_CP Pin of 74HC595(Pin12)
clockPin = 15  # SH_CP Pin of 74HC595(Pin11)
pic = [0x1c, 0x22, 0x51, 0x45, 0x45, 0x51, 0x22, 0x1c]  # data of smiling face
data = [  # data of "0-F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # " "
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x3E, 0x00, 0x00,  # "0"
    0x00, 0x00, 0x21, 0x7F, 0x01, 0x00, 0x00, 0x00,  # "1"
    0x00, 0x00, 0x23, 0x45, 0x49, 0x31, 0x00, 0x00,  # "2"
    0x00, 0x00, 0x22, 0x49, 0x49, 0x36, 0x00, 0x00,  # "3"
    0x00, 0x00, 0x0E, 0x32, 0x7F, 0x02, 0x00, 0x00,  # "4"
    0x00, 0x00, 0x79, 0x49, 0x49, 0x46, 0x00, 0x00,  # "5"
    0x00, 0x00, 0x3E, 0x49, 0x49, 0x26, 0x00, 0x00,  # "6"
    0x00, 0x00, 0x60, 0x47, 0x48, 0x70, 0x00, 0x00,  # "7"
    0x00, 0x00, 0x36, 0x49, 0x49, 0x36, 0x00, 0x00,  # "8"
    0x00, 0x00, 0x32, 0x49, 0x49, 0x3E, 0x00, 0x00,  # "9"
    0x00, 0x00, 0x3F, 0x44, 0x44, 0x3F, 0x00, 0x00,  # "A"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x36, 0x00, 0x00,  # "B"
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x22, 0x00, 0x00,  # "C"
    0x00, 0x00, 0x7F, 0x41, 0x41, 0x3E, 0x00, 0x00,  # "D"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x41, 0x00, 0x00,  # "E"
    0x00, 0x00, 0x7F, 0x48, 0x48, 0x40, 0x00, 0x00,  # "F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # " "
]


def setup():
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)


def shiftOut(dPin, cPin, val):
    for i in range(0, 8):
        GPIO.output(cPin, GPIO.LOW)
        GPIO.output(dPin, (0x80 & (val << i) == 0x80) and GPIO.HIGH or GPIO.LOW)
        GPIO.output(cPin, GPIO.HIGH)


def loop():
    while True:
        for j in range(0, 300):  # Repeat enough times to display the smiling face a period of time
            x = 0x80
            for i in range(0, 8):
                GPIO.output(latchPin, GPIO.LOW)
                shiftOut(dataPin, clockPin, pic[i])  # first shift data of line information to first stage 74HC959

                shiftOut(dataPin, clockPin, ~x)  # then shift data of column information to second stage 74HC959
                GPIO.output(latchPin, GPIO.HIGH)  # Output data of two stage 74HC595 at the same time
                time.sleep(0.001)  # display the next column
                x >>= 1
        for k in range(0, len(data) - 8):  # len(data) total number of "0-F" columns
            for j in range(0, 10):
                x = 0x80  # Set the column information to start from the first column
                for i in range(k, k + 8):
                    GPIO.output(latchPin, GPIO.LOW)
                    shiftOut(dataPin, clockPin, data[i])
                    shiftOut(dataPin, clockPin, ~x)
                    GPIO.output(latchPin, GPIO.HIGH)
                    time.sleep(0.001)
                    x >>= 1


img = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]


def display_img(bmp, length_seconds):
    bins = []
    for row in bmp:
        bin_num = 0
        for bit in row:
            bin_num = bin_num << 1
            if bit:
                bin_num += bit
        bins.append(bin_num)

    column_time = 0.001
    iterations = int(length_seconds // column_time // len(bins))
    for _ in range(iterations):
        for b in range(len(bins)):
            GPIO.output(latchPin, GPIO.LOW)
            shiftOut(dataPin, clockPin, bins[b])
            shiftOut(dataPin, clockPin, ~(0x01 << b))
            GPIO.output(latchPin, GPIO.HIGH)
            time.sleep(column_time)


def get_sin_image(t):
    out = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    y_step = 2 / 8
    y_offset = 4 * y_step
    x_step = y_step
    for x in range(8):
        y_val = int((math.sin(2 * (t + x) * x_step) + y_offset) / y_step)
        print(f"x={x}, y={y_val}")
        out[x][y_val] = 1

    return out


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    setup()
    try:
        # loop()
        for t in range(0, 100):
            display_img(get_sin_image(t), 0.05)
    finally:
        destroy()
