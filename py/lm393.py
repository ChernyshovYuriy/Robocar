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

        self.r_cm = 3.3
        self.dist_meas = 0.00
        self.km_per_hour = 0
        self.rpm = 0
        self.elapse = 0
        self.pulse = 0
        self.start_timer = time.time()

    def start(self):
        print("Start LM393")
        if self.is_run is True:
            return

        self.is_run = True
        self.dist_meas = 0.00
        self.km_per_hour = 0
        self.rpm = 0
        self.elapse = 0
        self.pulse = 0
        self.start_timer = time.time()
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

    def calculate(self):
        if self.elapse != 0:  # to avoid DivisionByZero error
            self.rpm = 1 / self.elapse * 60
            circ_cm = (2 * math.pi) * self.r_cm  # calculate wheel circumference in CM
            dist_km = circ_cm / 100000  # convert cm to km
            km_per_sec = dist_km / self.elapse  # calculate KM/sec
            km_per_hour = km_per_sec * 3600  # calculate KM/h
            dist_meas = (dist_km * self.pulse) * 1000  # measure distance traverse in meter
            print('rpm:{0:.0f}-RPM kmh:{1:.0f}-KMH dist_meas:{2:.2f}m pulse:{3}'.format(self.rpm, km_per_hour, dist_meas,
                                                                                        self.pulse))
        pass

    def right_sensor_callback(self, channel):
        print("Callback R")
        self.pulse += 1  # increase pulse by 1 whenever interrupt occurred
        self.elapse = time.time() - self.start_timer  # elapse for every 1 complete rotation made!
        self.start_timer = time.time()
        self.calculate()

    def left_sensor_callback(self, channel):
        print("Callback L")

    # Handle distance measurement.
    def runnable(self):
        GPIO.add_event_detect(GPIOManager.LM393_R, GPIO.FALLING, callback=self.right_sensor_callback, bouncetime=20)
        GPIO.add_event_detect(GPIOManager.LM393_L, GPIO.FALLING, callback=self.left_sensor_callback, bouncetime=20)
