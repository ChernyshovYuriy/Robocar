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
    TRIGGER_2 = 17
    ECHO_2 = 18
    # MOTOR_R_F = 5
    # MOTOR_R_B = 6

    @staticmethod
    def init():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIOManager.TRIGGER_1, GPIO.OUT)
            GPIO.setup(GPIOManager.TRIGGER_2, GPIO.OUT)
            GPIO.setup(GPIOManager.ECHO_1, GPIO.IN)
            GPIO.setup(GPIOManager.ECHO_2, GPIO.IN)

    @staticmethod
    def cleanup():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.cleanup()