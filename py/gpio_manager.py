import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


# Manager of the GPIO and its pins.
class GPIOManager:

    TRIGGER = 23
    ECHO = 24
    MOTOR_R_F = 17
    MOTOR_R_B = 16
    MOTOR_L_F = 5
    MOTOR_L_B = 6

    @staticmethod
    def init():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIOManager.TRIGGER, GPIO.OUT)
            GPIO.setup(GPIOManager.ECHO, GPIO.IN)
            GPIO.setup(GPIOManager.MOTOR_R_F, GPIO.OUT)
            GPIO.setup(GPIOManager.MOTOR_R_B, GPIO.OUT)
            GPIO.setup(GPIOManager.MOTOR_L_F, GPIO.OUT)
            GPIO.setup(GPIOManager.MOTOR_L_B, GPIO.OUT)

    @staticmethod
    def cleanup():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.cleanup()