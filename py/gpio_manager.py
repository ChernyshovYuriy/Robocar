import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


class GPIOManager:

    TRIGGER = 23
    ECHO = 24
    MOTOR_R_F = 11
    MOTOR_R_B = 15
    MOTOR_L_F = 16
    MOTOR_L_B = 18

    @staticmethod
    def init():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIOManager.TRIGGER, GPIO.OUT)
            GPIO.setup(GPIOManager.ECHO, GPIO.IN)

    @staticmethod
    def cleanup():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.cleanup()