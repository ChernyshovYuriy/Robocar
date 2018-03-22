import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import time
import py.config
from threading import Thread
from time import sleep
import statistics as stat

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO
    from py.gpio_manager import GPIOManager
    # from py.i2c_sonar import SonarSensor


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

    SENSORS = [(GPIOManager.TRIGGER_1, GPIOManager.ECHO_1),
               (GPIOManager.TRIGGER_2, GPIOManager.ECHO_2),
               (GPIOManager.TRIGGER_3, GPIOManager.ECHO_3)]

    def __init__(self, on_echo):
        print("Init  echo on ", py.config.CONFIG)
        self.is_run = False
        self.default_distance = 0
        self.thread = None
        self.on_echo = on_echo
        # Connect to local Pi.
        # self.pi = pigpio.pi()
        # self.sonar_sensor = SonarSensor(self.pi)

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
        # self.sonar_sensor.cancel()
        # self.pi.stop()

    # Handle distance measurement.
    def runnable(self):
        while self.is_run:
            distance = [[self.default_distance, self.default_distance, self.default_distance],
                        [self.default_distance, self.default_distance, self.default_distance],
                        [self.default_distance, self.default_distance, self.default_distance]]
            if py.config.CONFIG is py.config.Platform.PI:
                for i in range(len(Echo.SENSORS)):
                    # distance[i] = Echo.distance(Echo.SENSORS[i][0], Echo.SENSORS[i][1])
                    for j in range(3):
                        distance[i][j] = Echo.distance(Echo.SENSORS[i][0], Echo.SENSORS[i][1])
                    distance[i] = round(stat.mean(distance[i]), 0)
            print("ECHO %s" % distance)
            # self.on_echo(distance)
            sleep(0.1)

    # Get distance from sensor.
    @staticmethod
    def distance(trigger, echo):
        """
        The PING is triggered by a HIGH pulse of 10 or more microseconds.
        Give a short LOW pulse beforehand to ensure a clean HIGH pulse.
        """
        GPIO.output(trigger, GPIO.LOW)
        time.sleep(Echo.TWO_MICROSEC)
        GPIO.output(trigger, GPIO.HIGH)
        time.sleep(Echo.TWELVE_MICROSEC)
        GPIO.output(trigger, GPIO.LOW)

        start_time = time.time()
        stop_time = time.time()

        """ Save the time of signal emitted """
        while GPIO.input(echo) == 0:
            start_time = time.time()

        """ Save the time of signal received """
        while GPIO.input(echo) == 1:
            stop_time = time.time()

        """ Time difference between emitted and received signal """
        time_elapsed = stop_time - start_time
        """ Multiply with the speed of sound and divide by two (distance to and from object) """
        return (time_elapsed * Echo.SOUND_SPEED) / 2
