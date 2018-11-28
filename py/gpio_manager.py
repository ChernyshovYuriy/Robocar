import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


# Manager of the GPIO and its pins.
class GPIOManager:

    LM393 = 12

    @staticmethod
    def init():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIOManager.LM393, GPIO.IN)
            print("GPIO Manager initialized")

    @staticmethod
    def cleanup():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.cleanup()
            print("GPIO Manager cleaned up")