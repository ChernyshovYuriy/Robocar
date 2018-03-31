import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


# Manager of the GPIO and its pins.
class GPIOManager:

    TRIGGER_1 = 25
    ECHO_1 = 26
    TRIGGER_2 = 23
    ECHO_2 = 24
    TRIGGER_3 = 20
    ECHO_3 = 21
    TRIGGER_4 = 17
    ECHO_4 = 18
    TRIGGER_5 = 5
    ECHO_5 = 6
    SERVO = 4

    ULTRASONIC_SENSORS = [
        [TRIGGER_1, ECHO_1],
        [TRIGGER_2, ECHO_2],
        [TRIGGER_3, ECHO_3]
        # [TRIGGER_4, ECHO_4],
        # [TRIGGER_5, ECHO_5]
    ]

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