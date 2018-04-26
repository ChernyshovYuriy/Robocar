import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import time
import py.config
from threading import Thread
from time import sleep

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
    # Max counter for the echo back
    MAX_COUNTER = 10000

    def __init__(self, on_echo, echo_error_callback):
        print("Init  echo on ", py.config.CONFIG)
        self.is_run = False
        self.default_distance = 0
        self.thread = None
        self.on_echo = on_echo
        self.echo_error_callback = echo_error_callback
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
            distance = [0, 0, 0, 0, 0]
            if py.config.CONFIG is py.config.Platform.PI:
                for i in range(len(GPIOManager.ULTRASONIC_SENSORS)):
                    distance[i] = Echo.distance(
                        GPIOManager.ULTRASONIC_SENSORS[i][0], GPIOManager.ULTRASONIC_SENSORS[i][1]
                    )
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
        c = 0
        while GPIO.input(echo) == 0:
            start_time = time.time()
            # c += 1
            # if c == Echo.MAX_COUNTER:
            #     print("Brake echo 0 loop")
            #     break

        """ Save the time of signal received """
        c = 0
        while GPIO.input(echo) == 1:
            stop_time = time.time()
            # c += 1
            # if c == Echo.MAX_COUNTER:
            #     print("Brake echo 1 loop")
            #     stop_time = start_time = 0
            #     break

        """ Time difference between emitted and received signal """
        time_elapsed = stop_time - start_time
        """ Multiply with the speed of sound and divide by two (distance to and from object) """
        return int((time_elapsed * Echo.SOUND_SPEED) / 2)
