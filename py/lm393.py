import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import time, math
import RPi.GPIO as GPIO
from py.gpio_manager import GPIOManager


class LM393:

    NUM_OF_SENSORS = 2
    LEFT_SENSOR_ID = 0
    RIGHT_SENSOR_ID = 1
    SENSORS = [LEFT_SENSOR_ID, RIGHT_SENSOR_ID]

    def __init__(self, on_values):
        print("Init  LM393")
        self.is_run = False
        self.value = 0
        self.thread = None
        self.on_values_internal = on_values
        self.time_stamp = time.time()

        r_cm = 0.17                                               # should be radius of wheel or distance between two
                                                                  # pulse-holes in case of sensor read multi-holes trigger
                                                                  # (need better description).
        wheel_circumference_cm = (2.0 * math.pi) * r_cm           # calculate wheel circumference in cm
        self.wheel_circumference_m = wheel_circumference_cm / 100 # convert cm to m
        """
        Distance, in meters (m)
        """
        self.dist_meas = [0.00] * LM393.NUM_OF_SENSORS
        """
        Speed, in meters per second (m/s)
        """
        self.speed = [0] * LM393.NUM_OF_SENSORS
        self.rpm = [0] * LM393.NUM_OF_SENSORS
        self.pulse = [0] * LM393.NUM_OF_SENSORS
        self.start_timer = [time.time()] * LM393.NUM_OF_SENSORS
        # Delta time between events, in seconds
        self.event_delta = 0.5

    def start(self):
        print("Start LM393")
        if self.is_run is True:
            return

        self.is_run = True
        for i in range(LM393.NUM_OF_SENSORS):
            self.rpm[i] = 0
            self.pulse[i] = 0
            self.dist_meas[i] = 0.00
            self.speed[i] = 0
            self.start_timer[i] = time.time()
        self.time_stamp = time.time()
        """
        Workaround for the segmentation fault when remove events
        """
        if not GPIOManager.IS_LM393_CALLBACK_REGISTERED:
            GPIO.add_event_detect(
                GPIOManager.LM393_R, GPIO.FALLING, callback=self.right_sensor_callback, bouncetime=20
            )
            GPIO.add_event_detect(
                GPIOManager.LM393_L, GPIO.FALLING, callback=self.left_sensor_callback, bouncetime=20
            )
            GPIOManager.IS_LM393_CALLBACK_REGISTERED = True

    def stop(self):
        print("Stop  LM393")
        if self.is_run is False:
            return

        self.is_run = False
        """
        Workaround for the segmentation fault when remove events
        """
        # GPIO.remove_event_detect(GPIOManager.LM393_R)
        # GPIO.remove_event_detect(GPIOManager.LM393_L)

    def calculate(self, elapse, sensor_id):
        if elapse != 0:  # to avoid DivisionByZero error
            self.rpm[sensor_id] = 1 / elapse * 60
            # calculate m/sec
            self.speed[sensor_id] = self.wheel_circumference_m / elapse
            # measure distance traverse in meters
            self.dist_meas[sensor_id] = self.wheel_circumference_m * self.pulse[sensor_id]
            # dispatch event once in 0.5 sec
            if time.time() - self.time_stamp >= self.event_delta:
                print('RPM:{0:.0f} Speed:{1:.0f} m/sec Distance:{2:.2f}m Pulse:{3}'.format(
                    self.rpm[sensor_id], self.speed[sensor_id], self.dist_meas[sensor_id], self.pulse[sensor_id])
                )
                self.on_values_internal(self.rpm)
                self.time_stamp = time.time()

    def handle_callback(self, sensor_id):
        if not self.is_run:
            return
        # increase pulse by 1 whenever interrupt occurred
        self.pulse[sensor_id] += 1
        # elapse for every 1 complete rotation made
        elapse = time.time() - self.start_timer[sensor_id]
        self.start_timer[sensor_id] = time.time()
        self.calculate(elapse, sensor_id)

    def right_sensor_callback(self, channel):
        self.handle_callback(LM393.RIGHT_SENSOR_ID)

    def left_sensor_callback(self, channel):
        self.handle_callback(LM393.LEFT_SENSOR_ID)

