import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py.gpio_manager import GPIOManager
from threading import Thread
import py.config
import time, math

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

        self.r_cm = 1.1
        self.dist_meas = [0.00, 0.00]
        self.km_per_hour = [0, 0]
        self.rpm = [0, 0]
        self.pulse = [0, 0]
        self.start_timer = [time.time(), time.time()]

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

    def calculate(self, elapse, i):
        if elapse != 0:  # to avoid DivisionByZero error
            self.rpm[i] = 1 / elapse * 60
            circ_cm = (2 * math.pi) * self.r_cm  # calculate wheel circumference in CM
            dist_km = circ_cm / 100000  # convert cm to km
            km_per_sec = dist_km / elapse  # calculate KM/sec
            self.km_per_hour[i] = km_per_sec * 3600  # calculate KM/h
            self.dist_meas[i] = (dist_km * self.pulse[i]) * 1000  # measure distance traverse in meter
            print('RPM:{0:.0f} Speed:{1:.0f} Km/H Distance:{2:.2f}m Pulse:{3}'.format(
                self.rpm[i], self.km_per_hour[i], self.dist_meas[i], self.pulse[i])
            )

    def right_sensor_callback(self, channel):
        # increase pulse by 1 whenever interrupt occurred
        self.pulse[1] += 1
        # elapse for every 1 complete rotation made
        elapse = time.time() - self.start_timer[1]
        self.start_timer[1] = time.time()
        self.calculate(elapse, 1)

    def left_sensor_callback(self, channel):
        # increase pulse by 1 whenever interrupt occurred
        self.pulse[0] += 1
        # elapse for every 1 complete rotation made
        elapse = time.time() - self.start_timer[0]
        self.start_timer[0] = time.time()
        self.calculate(elapse, 0)

    # Handle distance measurement.
    def runnable(self):
        for i in range(2):
            self.rpm[i] = 0
            self.pulse[i] = 0
            self.dist_meas[i] = 0.00
            self.km_per_hour[i] = 0
            self.start_timer[i] = time.time()
        GPIO.add_event_detect(GPIOManager.LM393_R, GPIO.FALLING, callback=self.right_sensor_callback, bouncetime=20)
        GPIO.add_event_detect(GPIOManager.LM393_L, GPIO.FALLING, callback=self.left_sensor_callback, bouncetime=20)
