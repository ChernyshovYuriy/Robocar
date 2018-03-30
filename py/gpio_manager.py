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
    TRIGGER_3 = 5
    ECHO_3 = 6
    TRIGGER_4 = 25
    ECHO_4 = 26
    TRIGGER_5 = 20
    ECHO_5 = 21
    SERVO = 4

    @staticmethod
    def init():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIOManager.SERVO, GPIO.OUT)
            GPIO.setup(GPIOManager.TRIGGER_1, GPIO.OUT)
            GPIO.setup(GPIOManager.TRIGGER_2, GPIO.OUT)
            GPIO.setup(GPIOManager.TRIGGER_3, GPIO.OUT)
            GPIO.setup(GPIOManager.TRIGGER_4, GPIO.OUT)
            GPIO.setup(GPIOManager.TRIGGER_5, GPIO.OUT)
            GPIO.setup(GPIOManager.ECHO_1, GPIO.IN)
            GPIO.setup(GPIOManager.ECHO_2, GPIO.IN)
            GPIO.setup(GPIOManager.ECHO_3, GPIO.IN)
            GPIO.setup(GPIOManager.ECHO_4, GPIO.IN)
            GPIO.setup(GPIOManager.ECHO_5, GPIO.IN)
            print("GPIO Manager initialized")

    @staticmethod
    def cleanup():
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.cleanup()
            print("GPIO Manager cleaned up")