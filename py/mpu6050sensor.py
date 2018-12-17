import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from mpu6050 import mpu6050
from threading import Thread
from time import sleep
import math
import numpy


# MPU-6050 sensor.
class MPU6050:

    def __init__(self, on_mpu6050_values):
        print("Init  MPU6050")
        self.is_run = False
        self.thread = None
        self.i = 0
        self.num_of_iterations = 1
        self.accel_2d_array = [0.00] * self.num_of_iterations
        self.gyro_z_array = [0] * self.num_of_iterations
        self.on_mpu6050_values_int = on_mpu6050_values
        self.sensor = mpu6050(0x76)

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
        self.i = 0
        while self.is_run:
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
            sleep(1)
            self.accel_2d_array[self.i] = accel_2d
            self.gyro_z_array[self.i] = gyro_z
            self.i += 1
            if self.i == self.num_of_iterations:
                self.i = 0
                accel_2d_avg = numpy.mean(self.accel_2d_array)
                gyro_z_avg = numpy.mean(self.gyro_z_array)
                print("MPU-6050 accel:%.2f\tgyro z:%d" % (accel_2d_avg, gyro_z_avg))
                self.on_mpu6050_values_int(accel_2d_avg, gyro_z_avg)
                for j in range(self.num_of_iterations):
                    self.accel_2d_array[j] = 0.00
                    self.gyro_z_array[j] = 0

