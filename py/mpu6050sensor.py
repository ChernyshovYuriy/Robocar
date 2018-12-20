import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from mpu6050 import mpu6050
from threading import Thread
from time import sleep
import math


class MPU6050:
    """
    This class handles MPU-6050 sensor.
    """

    def __init__(self, on_mpu6050_values):
        print("Init  MPU6050 senor")
        self.is_run = False
        self.thread = None
        self.on_mpu6050_values_int = on_mpu6050_values
        self.sensor = mpu6050(0x68)

    # Start data fetch.
    def start(self):
        if self.is_run is True:
            return

        print("Start MPU-6050")
        self.is_run = True
        """Run echo in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable, name="MPU6050-Thread")
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
            sleep(1)
            # Reads the temperature from the onboard temperature sensor of the MPU-6050
            # temp = self.sensor.get_temp()
            # Gets and returns the X, Y and Z values from the accelerometer
            accel = self.sensor.get_accel_data(True)
            accel_x = accel['x']
            accel_y = accel['y']
            # accel_z = accel['z']
            # Gets and returns the X, Y and Z values from the gyroscope.
            gyro = self.sensor.get_gyro_data()
            gyro_z = gyro['z']
            # roll = math.atan2(accel['y'], accel['z']) * 180 / math.pi
            # pitch = math.atan2(-accel['x'], math.sqrt(accel['y'] * accel['y'] + accel['z'] * accel['z'])) * 180 / math.pi
            accel_2d = math.sqrt(accel_x ** 2 + accel_y ** 2)
            accel_2d = float("%0.2f" % accel_2d)
            # Use gyro Z to detect rotate left/right (positive/negative)
            # print(
            #     "MPU-6050 T:%d °C\taccel(x:%f,\ty:%f,\tz:%f,\tval:%.2f)\tgyro(x:%d,\ty:%d,\tz:%d)"
            #     % (temp, accel_x, accel_y, accel_z, accel_2d, gyro['x'], gyro['y'], gyro['z'])
            # )
            # print("MPU-6050 accel:%.2f\tgyro z:%d" % (accel_2d, gyro_z))
            # self.on_mpu6050_values_int(accel_2d, gyro_z)
            print("MPU-6050 accel:%.2f\tgyro z:%d" % (accel_2d, gyro_z))
            self.on_mpu6050_values_int(accel_2d, gyro_z)
