#!/usr/bin/env python3
########################################################################
# Filename    : Sweep.py
# Description : Servo sweep
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time

SERVO_MIN_DUTY = 2
SERVO_MAX_DUTY = 14
servoPin = 12
global p


def map(value, fromLow, fromHigh, toLow, toHigh):  # map a value from one range to another range
    return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow


def setup():
    global p
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(servoPin, GPIO.OUT)  # Set servoPin to OUTPUT mode
    GPIO.output(servoPin, GPIO.LOW)  # Make servoPin output LOW level

    p = GPIO.PWM(servoPin, 50)  # set Frequece to 50Hz
    p.start(0)  # Set initial Duty Cycle to 0


def servoWrite(angle):  # make the servo rotate to specific angle, 0-180
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    duty = map(angle, 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY)
    print(f"Writing duty cycle {duty} for angle {angle}")
    p.ChangeDutyCycle(duty)  # map the angle to duty cycle and output it


def loop():
    while True:
        # servoWrite(0)
        # time.sleep(1)
        # servoWrite(180)
        # time.sleep(1)

        step_pause = 0.01
        for angle in range(0, 180, 1):  # make servo rotate from 0 to 180 deg
            servoWrite(angle)  # Write angle value to servo
            time.sleep(step_pause)
        time.sleep(0.5)
        for angle in reversed(range(0, 180, 1)):  # make servo rotate from 180 to 0 deg
            servoWrite(angle)
            time.sleep(step_pause)
        time.sleep(0.5)


def destroy():
    p.stop()
    GPIO.cleanup()


if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
