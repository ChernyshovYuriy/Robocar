import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from time import sleep

import RPi.GPIO as GPIO

from py.PWM import RPi_PWM_Adapter

pwm = RPi_PWM_Adapter(GPIO)
pwm.start(4, 50)

pwm.set_duty_cycle(4, 0)
sleep(1)

while True:
    try:
        pwm.set_duty_cycle(4, 0)
        sleep(1)
        pwm.set_duty_cycle(4, 50)
        sleep(1)
        pwm.set_duty_cycle(4, 100)
        sleep(1)
        pwm.set_duty_cycle(4, 50)
        sleep(1)
    except KeyboardInterrupt:
        break

print("\nTidying up")

pwm.stop(4)
