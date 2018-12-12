import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py.octasonic import Octasonic
from threading import Thread
from time import sleep


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
    # Number of sensors
    SENSORS_NUM = 7

    def __init__(self, on_echo, echo_error_callback):
        print("Init  echo")
        self.is_run = False
        self.default_distance = 0
        self.thread = None
        self.on_echo = on_echo
        self.echo_error_callback = echo_error_callback
        factor = 1.5
        self.norm_weights = [2 * factor, 7 * factor, 12 * factor, 15 * factor, 12 * factor, 7 * factor, 2 * factor]
        self.octasonic = Octasonic(0)
        protocol_version = self.octasonic.get_protocol_version()
        firmware_version = self.octasonic.get_firmware_version()
        print("Octasonic protocol v%s firmware v%s" % (protocol_version, firmware_version))
        self.octasonic.set_sensor_count(Echo.SENSORS_NUM)

    # Whether echo is running
    def is_active(self):
        return self.is_run

    # Start echo location.
    def start(self):
        if self.is_run is True:
            return

        print("Start echo")
        self.octasonic.toggle_led()
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
        self.octasonic.toggle_led()
        self.is_run = False
        self.thread = None

    # Handle distance measurement.
    def runnable(self):
        while self.is_run:
            distance = [0] * Echo.SENSORS_NUM
            weights = [0] * Echo.SENSORS_NUM
            for i in range(Echo.SENSORS_NUM):
                distance[i] = self.octasonic.get_sensor_reading(i)
                weights[i] = distance[i]
            self.calculate_weights(weights)
            self.on_echo(distance, weights)
            sleep(0.1)

    def calculate_weights(self, weights):
        """
        Normalize
        """
        for i in range(len(weights)):
            if weights[i] >= self.norm_weights[i]:
                weights[i] = 1
            else:
                v = weights[i] / self.norm_weights[i]
                weights[i] = int(v * 10) / 10.0
        """
        Adjust move vector
        """
        for i in range(len(weights)):
            if weights[i] >= 1:
                continue
            if i == 0:
                weights[6] += (1 - weights[i])
            if i == 1:
                weights[5] += (1 - weights[i])
            if i == 2:
                weights[4] += (1 - weights[i])
            if i == 4:
                weights[2] += (1 - weights[i])
            if i == 5:
                weights[1] += (1 - weights[i])
            if i == 6:
                weights[0] += (1 - weights[i])
