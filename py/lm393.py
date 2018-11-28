import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from time import sleep
from py.gpio_manager import GPIOManager
from threading import Thread
import py.config
if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO

# Max counter for the echo back
LM393_MAX_COUNTER = 10000


class LM393:

    def __init__(self, on_value):
        print("Init  LM393")
        self.is_run = False
        self.value = 0
        self.thread = None
        self.on_value_int = on_value

    def start(self):
        print("Start LM393")
        if self.is_run is True:
            return

        self.is_run = True
        """Run LM393 in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable)
        self.thread.start()

    def stop(self):
        print("Stop  LM393")
        if self.is_run is False:
            return

        self.is_run = False
        self.thread = None

    # Handle distance measurement.
    def runnable(self):
        while self.is_run:
            left = 0
            right = self.get_value(GPIOManager.LM393_R)
            self.on_value_int(left, right)

    @staticmethod
    def get_value(pin):
        # print("\n-- start")
        count = 0

        # Output on the pin for
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        sleep(0.1)

        # Change the pin back to input
        GPIO.setup(pin, GPIO.IN)

        c = 0
        # Count until the pin goes high
        while count == 0 or GPIO.input(pin) == GPIO.LOW:
            count += 1
            c += 1
            if c == LM393_MAX_COUNTER:
                print("Brake lm393 loop")
                break
        # print("-- stop")
        return count
