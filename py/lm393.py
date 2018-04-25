import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from time import sleep
from py.gpio_manager import GPIOManager
import py.config
if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


class LM393:

    def __init__(self):
        print("Init  LM393")

    def start(self):
        print("Start LM393")
        try:
            # Main loop
            while True:
                print ("Count:" % self.callback())
        except KeyboardInterrupt:
            pass

    def stop(self):
        print("Stop  LM393")

    def callback(self):
        print("Callback LM393")
        count = 0

        # Output on the pin for
        GPIO.setup(GPIOManager.LM393, GPIO.OUT)
        GPIO.output(GPIOManager.LM393, GPIO.LOW)
        sleep(0.1)

        # Change the pin back to input
        GPIO.setup(GPIOManager.LM393, GPIO.IN)

        # Count until the pin goes high
        while GPIO.input(GPIOManager.LM393) == GPIO.LOW:
            count += 1

        return count
