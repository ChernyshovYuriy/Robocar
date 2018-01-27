import sys
from os.path import dirname, abspath
from time import sleep

sys.path.append(dirname(dirname(abspath(__file__))))

import time
from threading import Thread

import py.config

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


class Echo:

    default_distance = 0

    def __init__(self, on_echo):
        """Initialize class's data here"""
        print("Init  echo on ", py.config.CONFIG)
        self.is_run = False
        self.gpio_trigger = 23
        self.gpio_echo = 24
        self.thread = None
        self.on_echo = on_echo

        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.setmode(GPIO.BCM)
            # Set GPIO direction (IN / OUT)
            GPIO.setup(self.gpio_trigger, GPIO.OUT)
            GPIO.setup(self.gpio_echo, GPIO.IN)

    # Start echo location.
    def start(self):
        if self.is_run is True:
            return

        print("Start echo")
        self.is_run = True
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
        self.on_echo(Echo.default_distance)

    def runnable(self):
        while self.is_run:
            distance = Echo.default_distance
            if py.config.CONFIG is py.config.Platform.PI:
                distance = self.distance()
            self.on_echo(distance)
            sleep(0.1)

    def distance(self):
        # Set trigger to HIGH
        GPIO.output(self.gpio_trigger, True)

        # Set trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)

        start_time = time.time()
        stop_time = time.time()

        # Save start time
        while GPIO.input(self.gpio_echo) == 0:
            start_time = time.time()

        # Save time of arrival
        while GPIO.input(self.gpio_echo) == 1:
            stop_time = time.time()

        # time difference between start and arrival
        time_elapsed = stop_time - start_time
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (time_elapsed * 34300) / 2

        return distance
