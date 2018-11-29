import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


# Manager of the GPIO and its pins.
class GPIOManager:

    LM393_R = 12
    LM393_L = 13

    @staticmethod
    def init():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIOManager.LM393_R, GPIO.IN, GPIO.PUD_UP)
            GPIO.setup(GPIOManager.LM393_L, GPIO.IN, GPIO.PUD_UP)
            print("GPIO Manager initialized, ver. %d" % GPIO.VERSION)

    @staticmethod
    def cleanup():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.cleanup()
            print("GPIO Manager cleaned up")