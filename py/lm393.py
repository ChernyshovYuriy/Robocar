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

    @staticmethod
    def right_sensor_callback(channel):
        print("Callback R")

    @staticmethod
    def left_sensor_callback(channel):
        print("Callback L")

    # Handle distance measurement.
    def runnable(self):
        GPIO.add_event_detect(GPIOManager.LM393_R, GPIO.FALLING, callback=self.right_sensor_callback, bouncetime=20)
        GPIO.add_event_detect(GPIOManager.LM393_L, GPIO.FALLING, callback=self.left_sensor_callback, bouncetime=20)
        print("EXIT")
