import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import time
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
                print ("Count: %d" % self.callback())
        except KeyboardInterrupt:
            pass

    def stop(self):
        print("Stop  LM393")

    def callback(self):
        print("Callback LM393")
        millis = int(round(time.time() * 1000))
        newmillis = int(round(time.time() * 1000))
        soundPeack = 1
        while (newmillis <= (millis + int(1000))):
            # print newmillis - millis
            # print GPIO.input(4)
            if GPIO.input(GPIOManager.LM393):
                soundPeack = soundPeack + 1
                time.sleep(0.1)  # give 100 ms to gpio pin rest time
            newmillis = int(round(time.time() * 1000))

        return soundPeack
