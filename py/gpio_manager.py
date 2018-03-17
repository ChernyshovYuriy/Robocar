import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


# Manager of the GPIO and its pins.
class GPIOManager:

    TRIGGER_1 = 23
    ECHO_1 = 24
    MOTOR_R_F = 5
    MOTOR_R_B = 6
    MOTOR_L_F = 17
    MOTOR_L_B = 16

    @staticmethod
    def init():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIOManager.TRIGGER_1, GPIO.OUT)
            GPIO.setup(GPIOManager.ECHO_1, GPIO.IN)
            GPIO.setup(GPIOManager.MOTOR_R_F, GPIO.OUT)
            GPIO.setup(GPIOManager.MOTOR_R_B, GPIO.OUT)
            GPIO.setup(GPIOManager.MOTOR_L_F, GPIO.OUT)
            GPIO.setup(GPIOManager.MOTOR_L_B, GPIO.OUT)

    @staticmethod
    def cleanup():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.cleanup()