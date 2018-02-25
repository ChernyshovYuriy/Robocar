import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config
from py import config
from py.config import Commander
from py.ui_commander import UiCommander
from py.cmd_commander import CmdCommander
from tkinter import StringVar, Tk
from py.echo import Echo
from py.motors import Motors
from py.gpio_manager import GPIOManager


class Controller:

    def __init__(self, distance_prompt_in, motors_prompt_in):
        print("Init  controller on %s" % py.config.CONFIG)
        self.is_run = False
        self.distance = 0
        self.distance_origin = 0
        self.distance_drove = 0
        self.distance_prompt_ref = distance_prompt_in
        self.motors_prompt_ref = motors_prompt_in
        self.echo = Echo(self.on_echo)
        self.motors = Motors(
            self.on_motors_stopped, self.on_motors_started, self.on_motors_turning
        )

    # Start controller.
    def start(self):
        if self.is_run is True:
            return

        print("Start controller")
        self.echo.start()
        self.motors.start()
        self.is_run = True

    # Stop controller
    def stop(self):
        if self.is_run is False:
            return

        print("Stop  controller")
        self.is_run = False
        self.motors.stop()
        self.echo.stop()

    # Run engine forward
    def eng_fwd(self):
        print("Engine forward")
        self.motors.forward()

    # Run engine backward
    def eng_bwd(self):
        print("Engine backward")
        self.motors.backward()

    # Run engine stop
    def eng_stop(self):
        print("Engine stop")
        self.motors.stop()

    # Callback function to echo class
    def on_echo(self, distance):
        print(" -- echo: %.1f" % distance)
        self.distance = distance
        self.motors.on_echo(self.distance)
        if config.COMMANDER is Commander.UI:
            self.distance_prompt_ref.set("Distance: %.1f cm" % self.distance)
        if self.distance_origin > 0:
            self.distance_drove = self.distance_origin - self.distance

    def on_motors_stopped(self):
        print(" -- motors stopped, drove %.1f sm" % self.distance_drove)
        self.distance_origin = 0
        """ Reset drove distance here, any reference must be obtained prior to this line """
        self.distance_drove = 0
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors stopped")

    def on_motors_started(self, state):
        print(" -- motors started %s, distance origin %.1f sm" % (state, self.distance))
        self.distance_origin = self.distance
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors started")

    def on_motors_turning(self):
        print(" -- motors turning")
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors Turning")


if __name__ == "__main__":
    print("Robocar started on %s, commander is %s" % (py.config.CONFIG, config.COMMANDER))
    GPIOManager.init()

    distance_prompt = None
    motors_prompt = None

    controller = Controller(distance_prompt, motors_prompt)

    if config.COMMANDER is Commander.CMD:
        commander = CmdCommander(controller)
    elif config.COMMANDER is Commander.UI:
        root = Tk()
        distance_prompt = StringVar()
        motors_prompt = StringVar()
        commander = UiCommander(controller, root, distance_prompt, motors_prompt)

    GPIOManager.cleanup()

    print("Robocar stopped")
