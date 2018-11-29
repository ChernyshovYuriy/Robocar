import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

# from mpu6050 import mpu6050
from threading import Thread
from time import sleep


# MPU-6050 sensor.
class MPU6050:

    def __init__(self):
        print("Init  echo")
        self.is_run = False
        self.thread = None
        self.sensor = mpu6050(0x68)

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
            accel_x, accel_y, accel_z = self.sensor.get_accel_data()
            # Gets and returns the X, Y and Z values from the gyroscope.
            gyro_x, gyro_y, gyro_z = self.sensor.get_gyro_data()
            print("MPU-6050 temp:%d" % (temp))
            sleep(0.5)

