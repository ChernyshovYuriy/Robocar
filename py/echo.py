import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import time
import py.config
from py.gpio_manager import GPIOManager
from threading import Thread
from time import sleep

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


# Ultra sonic locator.
class Echo:

    # Speed of sound, im cm/sec
    SOUND_SPEED = 34300

    def __init__(self, on_echo):
        print("Init  echo on ", py.config.CONFIG)
        self.is_run = False
        self.default_distance = 0
        self.thread = None
        self.on_echo = on_echo

    # Start echo location.
    def start(self):
        if self.is_run is True:
            return

        print("Start echo")
        self.is_run = True
        """Run echo in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable)
        self.thread.start()

    # Stop echo location
    def stop(self):
        if self.is_run is False:
            return

        print("Stop  echo")
        self.is_run = False
        self.thread = None

    # Handle distance measurement.
    def runnable(self):
        while self.is_run:
            distance = self.default_distance
            if py.config.CONFIG is py.config.Platform.PI:
                distance = Echo.distance()
            self.on_echo(distance)
            sleep(0.1)

    # Get distance from sensor.
    @staticmethod
    def distance():
        GPIO.output(GPIOManager.TRIGGER, True)

        time.sleep(0.00001)
        GPIO.output(GPIOManager.TRIGGER, False)

        start_time = time.time()
        stop_time = time.time()

        """ Save the time of signal emitted """
        while GPIO.input(GPIOManager.ECHO) == 0:
            start_time = time.time()

        """ Save the time of signal received """
        while GPIO.input(GPIOManager.ECHO) == 1:
            stop_time = time.time()

        """ Time difference between emitted and received signal """
        time_elapsed = stop_time - start_time
        """ Multiply with the speed of sound and divide by two (distance to and from object) """
        distance = (time_elapsed * Echo.SOUND_SPEED) / 2

        return distance
