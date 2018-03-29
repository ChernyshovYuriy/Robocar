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
from py.i2c_manager import I2CManager

import RPi.GPIO as GPIO
from time import sleep


class Controller:

    def __init__(self, distance_prompt_in, motors_prompt_in):
        print("Init  controller on %s" % py.config.CONFIG)
        self.is_run = False
        self.distance = [0, 0, 0]
        self.distance_origin = [0, 0, 0]
        self.distance_drove = 0
        self.distance_prompt_ref = distance_prompt_in
        self.motors_prompt_ref = motors_prompt_in
        self.echo = Echo(self.on_echo)
        self.motors = Motors(
            self.on_motors_stopped, self.on_motors_started, self.on_motors_turning
        )
        self.pwm = None


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

    # Run engines turn left
    def eng_turn_l(self):
        print("Engines turn left")
        self.motors.turn_l()

    # Run engines turn right
    def eng_turn_r(self):
        print("Engines turn right")
        self.motors.turn_r()

    # Run engine stop
    def eng_stop(self):
        print("Engine stop")
        self.motors.stop_motors()

    # Run debug action
    def run_debug(self):
        print("Run debug")
        if self.pwm is None:
            self.pwm = GPIO.PWM(GPIOManager.SERVO, 50)
            self.pwm.start(0)
            print("PWM Initialized")

        self.SetAngle(90)
        sleep(1)
        self.SetAngle(0)
        # self.pwm.stop()

    def SetAngle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(GPIOManager.SERVO, 1)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(GPIOManager.SERVO, 0)
        self.pwm.ChangeDutyCycle(0)

    # Callback function to echo class
    def on_echo(self, distance):
        print(" -- echo: %s" % distance)
        self.distance = distance
        self.motors.on_echo(self.distance)
        if config.COMMANDER is Commander.UI:
            self.distance_prompt_ref.set("Distance: %s cm" % self.distance)
        # if self.distance_origin > 0:
            # self.distance_drove = self.distance_origin - self.distance

    def on_motors_stopped(self):
        print(" -- motors stopped, drove %.1f sm" % self.distance_drove)
        self.distance_origin = [0, 0, 0]
        """ Reset drove distance here, any reference must be obtained prior to this line """
        # self.distance_drove = 0
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors stopped")

    def on_motors_started(self, state):
        print(" -- motors started %s, distance origin %s sm" % (state, self.distance))
        self.distance_origin = self.distance
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors started")

    def on_motors_turning(self, state):
        print(" -- motors turning %s" % state)
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors Turning")


if __name__ == "__main__":
    print("Robocar started on %s, commander is %s" % (py.config.CONFIG, config.COMMANDER))
    GPIOManager.init()
    I2CManager.init()

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
    I2CManager.cleanup()

    print("Robocar stopped")
