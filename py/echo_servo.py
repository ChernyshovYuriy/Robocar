import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py.gpio_manager import GPIOManager
import py.config
from threading import Thread
import time

if py.config.CONFIG is py.config.Platform.PI:
    import pigpio


#
class EchoServo:

    SLEEP_TIME = 0.15
    STEPS = [500, 833, 1166, 1500, 1833, 2166, 2500]

    def __init__(self):
        print("Init servo echo on ", py.config.CONFIG)
        self.is_run = False
        self.thread = None
        self.pi = None

    # Start
    def start(self):
        if self.is_run is True:
            return

        print("Start servo echo")
        self.is_run = True
        self.pi = pigpio.pi()
        self.pi.set_servo_pulsewidth(GPIOManager.SERVO, 500)
        """Run servo echo in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable)
        self.thread.start()

    # Stop
    def stop(self):
        if self.is_run is False:
            return

        print("Stop servo echo")
        self.is_run = False
        self.thread = None

    #
    def runnable(self):
        idx = 0
        direction = True
        while self.is_run:
            # print("Step:%d" % steps[idx])
            self.pi.set_servo_pulsewidth(GPIOManager.SERVO, EchoServo.STEPS[idx])
            time.sleep(EchoServo.SLEEP_TIME)

            if direction:
                idx += 1
            else:
                idx -= 1
            if idx == len(EchoServo.STEPS) - 1:
                direction = False
            if idx == 0:
                direction = True
