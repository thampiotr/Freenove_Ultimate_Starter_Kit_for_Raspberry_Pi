#!/usr/bin/env python3
#############################################################################
# Filename    : Motor.py
# Description : Control Motor with L293D
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time

# define the pins connected to L293D
import smbus

motoRPin1 = 13  # GPIO 27
motoRPin2 = 11  # GPIO 17
enablePin = 15  # GPIO 22


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


global adc, p


def setup():
    global adc
    adc = PCF8591()
    global p
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motoRPin1, GPIO.OUT)  # set pins to OUTPUT mode
    GPIO.setup(motoRPin2, GPIO.OUT)
    GPIO.setup(enablePin, GPIO.OUT)

    p = GPIO.PWM(enablePin, 1000)  # creat PWM and set Frequence to 1KHz
    p.start(0)


# mapNUM function: map the value from a range of mapping to another range.
def mapNUM(value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow


# motor function: determine the direction and speed of the motor according to the input ADC value input
def motor(ADC):
    value = ADC - 128
    if 10 > value > -10:
        GPIO.output(motoRPin1, GPIO.LOW)
        GPIO.output(motoRPin2, GPIO.LOW)
        print('Motor Stop...')
        duty_cycle = 0
    elif value > 10:  # make motor turn forward
        GPIO.output(motoRPin1, GPIO.HIGH)  # motoRPin1 output HIHG level
        GPIO.output(motoRPin2, GPIO.LOW)  # motoRPin2 output LOW level
        print('Turn Forward...')
        duty_cycle = mapNUM(abs(value), 0, 128, 0, 100)
    else:  # make motor turn backward
        GPIO.output(motoRPin1, GPIO.LOW)
        GPIO.output(motoRPin2, GPIO.HIGH)
        print('Turn Backward...')
        duty_cycle = mapNUM(abs(value), 0, 128, 0, 100)
    p.ChangeDutyCycle(duty_cycle)
    print('The PWM duty cycle is %d%%\n' % duty_cycle)  # print PMW duty cycle.


def loop():
    while True:
        value = adc.analogRead(0)  # read ADC value of channel 0
        print('ADC Value : %d' % (value))
        motor(value)
        time.sleep(0.01)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    print('Program is starting... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
