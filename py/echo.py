import sys
from os.path import dirname, abspath

from py.i2c_manager import I2CManager

sys.path.append(dirname(dirname(abspath(__file__))))

import time
import py.config
from threading import Thread
from time import sleep

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


# Ultra sonic locator.
class Echo:

    # Speed of sound, im cm/sec
    # tempAir = 24.0;
    # soundSpeed = 331.3 + 0.06 * tempAir; is 332.74 m / s
    SOUND_SPEED = 33274
    # 2 microseconds
    TWO_MICROSEC = 0.000002
    # 12 microseconds
    TWELVE_MICROSEC = 0.000012

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
        self.on_echo(self.default_distance)

    # Handle distance measurement.
    def runnable(self):
        while self.is_run:
            distance = self.default_distance
            # sample = []
            if py.config.CONFIG is py.config.Platform.PI:
                # for i in range(5):
                    distance = Echo.distance()
                    # if distance > 0:
                    #     sample.append(distance)
                    #     print("   TRACE :: %d" % distance)
                    # sleep(0.1)
                # sample = sorted(sample)
            # res = sample[0]
            # print("TRACE %d" % res)
            self.on_echo(distance)
            sleep(0.1)

    # Get distance from sensor.
    @staticmethod
    def distance():
        """
        The PING is triggered by a HIGH pulse of 10 or more microseconds.
        Give a short LOW pulse beforehand to ensure a clean HIGH pulse.
        """
        I2CManager.output(I2CManager.TRIGGER_2, GPIO.LOW)
        time.sleep(Echo.TWO_MICROSEC)
        I2CManager.output(I2CManager.TRIGGER_2, GPIO.HIGH)
        time.sleep(Echo.TWELVE_MICROSEC)
        I2CManager.output(I2CManager.TRIGGER_2, GPIO.LOW)

        start_time = time.time()
        stop_time = time.time()

        """ Save the time of signal emitted """
        while I2CManager.input(I2CManager.ECHO_2) == 0:
            start_time = time.time()

        """ Save the time of signal received """
        while I2CManager.input(I2CManager.ECHO_2) == 1:
            stop_time = time.time()

        """ Time difference between emitted and received signal """
        time_elapsed = stop_time - start_time
        """ Multiply with the speed of sound and divide by two (distance to and from object) """
        distance = (time_elapsed * Echo.SOUND_SPEED) / 2

        return distance
