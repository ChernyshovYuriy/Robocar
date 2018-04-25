import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from time import sleep
from py.gpio_manager import GPIOManager
from threading import Thread
import py.config
if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


class LM393:

    def __init__(self):
        print("Init  LM393")
        self.is_run = False
        self.value = 0
        self.thread = None

    def start(self):
        print("Start LM393")
        if self.is_run is True:
            return

        print("Start echo")
        self.is_run = True
        """Run echo in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable)
        self.thread.start()

    def stop(self):
        print("Stop  LM393")
        if self.is_run is False:
            return

        print("Stop  echo")
        self.is_run = False
        self.thread = None

    # Handle distance measurement.
    def runnable(self):
        while self.is_run:
            value = self.get_value()
            print("Value %d" % value)

    def get_value(self):
        print("Callback LM393")
        count = 0

        # Output on the pin for
        GPIO.setup(GPIOManager.LM393, GPIO.OUT)
        GPIO.output(GPIOManager.LM393, GPIO.LOW)
        sleep(0.1)

        # Change the pin back to input
        GPIO.setup(GPIOManager.LM393, GPIO.IN)

        # Count until the pin goes high
        while GPIO.input(GPIOManager.LM393) == GPIO.LOW:
            count += 1

        return count
