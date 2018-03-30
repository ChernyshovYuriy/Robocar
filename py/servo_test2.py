from time import sleep

import RPi

from py import PWM

pwm = PWM.RPi_PWM_Adapter(RPi.GPIO)
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
