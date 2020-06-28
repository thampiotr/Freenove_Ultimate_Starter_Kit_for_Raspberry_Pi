import time

import pigpio

p = pigpio.pi()
pin = 18

# For my servo, I found:
# 50Hz -> 2 to 12 dc
# 100Hz -> 4 to 24 dc
# 200Hz -> 8 to 48 dc
# 400Hz -> 16 to 96 dc

frequency = 400
pwm_range = 100
min_duty = 16
max_duty = 96
sleep_time = 0.01

print(f'range: {p.get_PWM_range(pin)}')
print(f'set range: {p.set_PWM_range(pin, pwm_range)}')

p.hardware_PWM(pin, frequency, min_duty)

# p.set_mode(pin, pigpio.ALT5)
# print('setting range:')
# print(p.set_PWM_range(pin, 100))

print(f'setting freq: {p.set_PWM_frequency(pin, frequency)}')
print(f'duty cycle: {p.get_PWM_dutycycle(pin)}')
print(f'frequency: {p.get_PWM_frequency(pin)}')

print('---------- SETUP ----------')
print(f'set duty cycle result: {p.set_PWM_dutycycle(pin, min_duty)}')
print(f'duty cycle: {p.get_PWM_dutycycle(pin)}')
print(f'frequency: {p.get_PWM_frequency(pin)}')

try:
    while True:
        for i in range(min_duty, max_duty, 1):
            p.set_PWM_dutycycle(pin, i)
            time.sleep(sleep_time)

        for i in reversed(range(min_duty, max_duty, 1)):
            p.set_PWM_dutycycle(pin, i)
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass
finally:
    print('---------- RESET ----------')
    p.set_PWM_dutycycle(pin, min_duty)
    time.sleep(1)
    print('---------- Clean up ----------')
    p.set_PWM_dutycycle(pin, 0)
    p.stop()
