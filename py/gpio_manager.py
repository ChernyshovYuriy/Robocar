import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import RPi.GPIO as GPIO


class GPIOManager:
    """
    Manager of the GPIO and its pins.
    """

    LM393_R = 12
    LM393_L = 13

    """
    Workaround for the segmentation fault when remove events
    """
    IS_LM393_CALLBACK_REGISTERED = False

    @staticmethod
    def init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIOManager.LM393_R, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(GPIOManager.LM393_L, GPIO.IN, GPIO.PUD_UP)
        print("GPIO Manager initialized, ver. %s" % GPIO.VERSION)

    @staticmethod
    def cleanup():
        if GPIOManager.IS_LM393_CALLBACK_REGISTERED:
            GPIO.remove_event_detect(GPIOManager.LM393_R)
            GPIO.remove_event_detect(GPIOManager.LM393_L)
            print("GPIO Manager clean LM393 callbacks")
        GPIO.cleanup()
        print("GPIO Manager cleaned up")