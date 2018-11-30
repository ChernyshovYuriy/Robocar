import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from mpu6050 import mpu6050
from threading import Thread
from time import sleep
import math


# MPU-6050 sensor.
class MPU6050:

    def __init__(self):
        print("Init  echo")
        self.is_run = False
        self.thread = None
        self.sensor = mpu6050(0x68)
        accel_range = self.sensor.read_accel_range()
        print("Accel range:%d" % accel_range)

    # Start data fetch.
    def start(self):
        if self.is_run is True:
            return

        print("Start MPU-6050")
        self.is_run = True
        """Run echo in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable)
        self.thread.start()

    # Stop data fetch
    def stop(self):
        if self.is_run is False:
            return

        print("Stop  MPU-6050")
        self.is_run = False
        self.thread = None

    # Handle data fetch.
    def runnable(self):
        while self.is_run:
            # Reads the temperature from the onboard temperature sensor of the MPU-6050
            temp = self.sensor.get_temp()
            # Gets and returns the X, Y and Z values from the accelerometer
            accel = self.sensor.get_accel_data(True)
            accel_x = accel['x']
            accel_y = accel['y']
            accel_z = accel['z']
            # Gets and returns the X, Y and Z values from the gyroscope.
            gyro = self.sensor.get_gyro_data()
            # roll = math.atan2(accel['y'], accel['z']) * 180 / math.pi
            # pitch = math.atan2(-accel['x'], math.sqrt(accel['y'] * accel['y'] + accel['z'] * accel['z'])) * 180 / math.pi
            acceleration = math.sqrt(accel_x ** 2 + accel_y ** 2 + accel_z ** 2)
            # Use gyro Z to detect rotate left/right (positive/negative)
            print(
                "MPU-6050 T:%d °C\taccel(x:%f,\ty:%f,\tz:%f,\tval:%f)\tgyro(x:%d,\ty:%d,\tz:%d)"
                % (temp, accel_x, accel_y, accel_z, acceleration, gyro['x'], gyro['y'], gyro['z'])
            )
            sleep(0.05)

