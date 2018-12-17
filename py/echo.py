import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py.octasonic import Octasonic
from threading import Thread
from time import sleep


class Echo:
    """
    Ultra sonic locator.
    """

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
        factor = 2
        self.norm_weights = [2, 3 * factor, 8 * factor, 10 * factor, 8 * factor, 3 * factor, 2]
        self.octasonic = Octasonic(0)
        protocol_version = self.octasonic.get_protocol_version()
        firmware_version = self.octasonic.get_firmware_version()
        print("Octasonic protocol v%s firmware v%s" % (protocol_version, firmware_version))
        self.octasonic.set_sensor_count(Echo.SENSORS_NUM)

    def is_active(self):
        """
        Whether or not echo is running.
        :return:
        """
        return self.is_run

    def start(self):
        """
        Start echo location.
        :return:
        """
        if self.is_run is True:
            return

        print("Start echo")
        self.octasonic.toggle_led()
        self.is_run = True
        """Run echo in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable)
        self.thread.start()

    def stop(self):
        """
        Stop echo location/
        :return:
        """
        if self.is_run is False:
            return

        print("Stop  echo")
        self.octasonic.toggle_led()
        self.is_run = False
        self.thread = None

    def runnable(self):
        """
        Handle distance measurement.
        :return:
        """
        while self.is_run:
            sleep(0.1)
            distance = [0] * Echo.SENSORS_NUM
            weights = [0.0] * Echo.SENSORS_NUM
            for i in range(Echo.SENSORS_NUM):
                distance[i] = self.octasonic.get_sensor_reading(i)
                weights[i] = distance[i]
            self.calculate_weights(weights)
            self.on_echo(distance, weights)

    def calculate_weights(self, weights):
        """
        Calculate weights for each sensor.
        """

        """
        Normalize
        """
        for i in range(len(weights)):
            if weights[i] >= self.norm_weights[i]:
                weights[i] = 1.0
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
