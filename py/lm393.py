import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py.gpio_manager import GPIOManager
import py.config
if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


class LM393:

    def __init__(self):
        print("Init  LM393")

    def start(self):
        print("Start LM393")
        GPIO.add_event_detect(GPIOManager.LM393, GPIO.RISING, callback=self.callback, bouncetime=300)

    def stop(self):
        print("Stop  LM393")

    def callback(self):
        print("Callback LM393")