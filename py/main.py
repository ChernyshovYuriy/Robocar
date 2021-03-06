import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py.httpserver import HttpServer, HttpServerData
from py import config
from py.config import Commander
from py.ui_commander import UiCommander
from py.cmd_commander import CmdCommander
from tkinter import StringVar, Tk
from py.echo import Echo
from py.mpu6050sensor import MPU6050
# from py.echo_servo import EchoServo
from py.motors import Motors, MotorsState
from py.gpio_manager import GPIOManager
from py.i2c_manager import I2CManager
from py.lm393 import LM393
from py.camera import Camera


class Controller:
    """
    Main controller of the Robocar.
    """

    def __init__(self, distance_prompt_in, motors_prompt_in):
        print("Init  controller")
        self.is_run = False
        self.distance_prompt_ref = distance_prompt_in
        self.motors_prompt_ref = motors_prompt_in
        self.echo = Echo(self.on_echo)
        # self.echo_servo = EchoServo()
        self.mpu6050sensor = MPU6050(self.on_mpu6050_values)
        self.lm393 = LM393(self.on_lm393_values)
        self.motors = Motors(
            self.on_motors_stopped, self.on_motors_started, self.on_motors_turning
        )
        self.camera = Camera()
        self.server_data = HttpServerData()
        self.server = HttpServer(self.server_data, self)

        self.camera.start()
        self.server.start()

    # Start controller.
    def start(self):
        if self.is_run is True:
            return

        print("Start controller")
        self.echo.start()
        self.camera.start()
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
        self.motors.stop()
        self.echo.stop()
        self.camera.stop()
        self.server.stop()
        # self.echo_servo.stop()

    # Run engine forward
    def eng_fwd(self):
        print("Motors forward")
        self.motors.set_state(MotorsState.START_FWD)
        self.motors.exec_cmd()

    # Run engine backward
    def eng_bwd(self):
        print("Motors backward")
        self.motors.set_state(MotorsState.START_BWD)
        self.motors.exec_cmd()

    # Run engines turn left
    def eng_turn_l(self):
        print("Motors turn left")
        self.motors.set_state(MotorsState.TURN_L)
        self.motors.exec_cmd()

    # Run engines turn right
    def eng_turn_r(self):
        print("Motors turn right")
        self.motors.set_state(MotorsState.TURN_R)
        self.motors.exec_cmd()

    # Run engine stop
    def eng_stop(self):
        print("Engine stop")
        self.motors.set_state(MotorsState.STOP)
        self.motors.exec_cmd()

    # Run print echo action
    def trigger_print_echo(self):
        if not self.echo.is_run:
            self.echo.start()
        else:
            self.echo.stop()
        pass

    # Run print gyro data
    def trigger_print_gyro_data(self):
        if not self.mpu6050sensor.is_run:
            self.mpu6050sensor.start()
        else:
            self.mpu6050sensor.stop()

    # Run print LM393 data
    def trigger_print_lm393_data(self):
        if not self.lm393.is_run:
            self.lm393.start()
        else:
            self.lm393.stop()

    # Callback function to LM393 class
    def on_lm393_values(self, rpm):
        self.motors.on_rpm(rpm)

    def on_mpu6050_values(self, accel, gyro_z):

        pass

    # Callback function to echo class
    def on_echo(self, distance, weights):
        print(" -- echo   : %s" % distance)
        print(" -- weights: %s" % weights)
        self.server_data.echo = distance
        self.motors.on_echo(distance, weights)
        if config.COMMANDER is Commander.UI:
            self.distance_prompt_ref.set("Distance: %s cm" % distance)

    def on_motors_stopped(self):
        print(" -- motors stopped")
        self.lm393.stop()
        self.mpu6050sensor.stop()
        """ Reset drove distance here, any reference must be obtained prior to this line """
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors stopped")

    def on_motors_started(self, state):
        print(" -- motors started %s" % (state))
        self.lm393.start()
        self.mpu6050sensor.start()
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors started")

    def on_motors_turning(self, state):
        print(" -- motors turning %s" % state)
        self.lm393.start()
        self.mpu6050sensor.start()
        if config.COMMANDER is Commander.UI:
            self.motors_prompt_ref.set("Motors Turning")


if __name__ == "__main__":
    print("Robocar started, commander is %s" % config.COMMANDER)
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

    controller.force_stop()
    GPIOManager.cleanup()
    I2CManager.cleanup()

    print("Robocar stopped")
