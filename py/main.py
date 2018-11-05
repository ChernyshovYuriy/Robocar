import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config
from py.httpserver import HttpServer, HttpServerData
from py import config
from py.config import Commander
from py.ui_commander import UiCommander
from py.cmd_commander import CmdCommander
from tkinter import StringVar, Tk
from py.echo import Echo
# from py.echo_servo import EchoServo
from py.motors import Motors, MotorsState
from py.gpio_manager import GPIOManager
from py.i2c_manager import I2CManager
# from py.lm393 import LM393
# from py.camera import Camera


class Controller:

    def __init__(self, distance_prompt_in, motors_prompt_in):
        print("Init  controller on %s" % py.config.CONFIG)
        self.is_run = False
        self.distance = [0] * Echo.SENSORS_NUM
        self.distance_prompt_ref = distance_prompt_in
        self.motors_prompt_ref = motors_prompt_in
        self.echo = Echo(self.on_echo, self.echo_error_callback)
        # self.echo_servo = EchoServo()
        self.motors = Motors(
            self.on_motors_stopped, self.on_motors_started, self.on_motors_turning
        )
        self.p = None
        # self.lm393 = LM393(self.on_lm393_value)
        # self.camera = Camera()
        self.server_data = HttpServerData()
        self.server = HttpServer(self.server_data)

        # self.camera.start()
        self.server.start()

    # Start controller.
    def start(self):
        if self.is_run is True:
            return

        print("Start controller")
        self.echo.start()
        # self.lm393.start()
        # self.camera.start()
        self.server.start()
        # self.echo_servo.start()
        self.motors.start()
        self.is_run = True

    # Stop controller
    def stop(self):
        if self.is_run is False:
            return

        print("Stop  controller")
        self.force_stop()

    # Force stop controller
    def force_stop(self):
        self.is_run = False
        # self.lm393.stop()
        self.motors.stop()
        self.echo.stop()
        # self.camera.stop()
        self.server.stop()
        # self.echo_servo.stop()

    # Run engine forward
    def eng_fwd(self):
        print("Engine forward")
        self.motors.set_state(MotorsState.START_FWD)
        self.motors.exec_cmd()

    # Run engine backward
    def eng_bwd(self):
        print("Engine backward")
        self.motors.set_state(MotorsState.STAR_BWD)
        self.motors.exec_cmd()

    # Run engines turn left
    def eng_turn_l(self):
        print("Engines turn left")
        self.motors.set_state(MotorsState.TURN_L)
        self.motors.exec_cmd()

    # Run engines turn right
    def eng_turn_r(self):
        print("Engines turn right")
        self.motors.set_state(MotorsState.TURN_R)
        self.motors.exec_cmd()

    # Run engine stop
    def eng_stop(self):
        print("Engine stop")
        self.motors.set_state(MotorsState.STOP)
        self.motors.exec_cmd()

    def echo_error_callback(self):
        print("Echo error")

    # Run print echo action
    def trigger_print_echo(self):
        if not self.echo.is_run:
            self.echo.start()
        else:
            self.echo.stop()
        print("ECHO :: ---> %s" % (self.distance))

    # Callback function to LM393 class
    # def on_lm393_value(self, value):
    #     print("LM393 value is %d" % value)
    #     self.motors.set_lm393_value(value)

    # Callback function to echo class
    def on_echo(self, distance):
        print(" -- echo: %s" % distance)
        self.distance = distance
        self.server_data.echo = distance
        self.motors.on_echo(self.distance)
        if config.COMMANDER is Commander.UI:
            self.distance_prompt_ref.set("Distance: %s cm" % self.distance)

    def on_motors_stopped(self):
        print(" -- motors stopped")
        """ Reset drove distance here, any reference must be obtained prior to this line """
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors stopped")

    def on_motors_started(self, state):
        print(" -- motors started %s" % (state))
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
