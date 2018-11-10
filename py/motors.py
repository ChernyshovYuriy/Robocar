import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py.echo import Echo
import py.config
from enum import Enum

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO
    from py.i2c_manager import I2CManager


# Enumeration of the motors states.
class MotorsState(Enum):
    STOP = 1
    START_FWD = 2
    START_BWD = 3
    TURN_L = 4
    TURN_R = 5


# Interface
class Command:

    def execute(self, listener):
        raise NotImplementedError()


# Stop motors command
class StopCmd(Command):

    def execute(self, reference):
        print("Motor - Stopped command")
        reference.stop_motors()


# Start motors forward command
class StartFwdCmd(Command):

    def execute(self, reference):
        print("Motor - Started fwd command")
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_R_F, GPIO.HIGH)
            I2CManager.output(I2CManager.MOTOR_L_F, GPIO.HIGH)
        reference.on_motors_started_ref(reference.get_state())


# Start motors backward command
class StartBwdCmd(Command):

    def execute(self, reference):
        print("Motor - Started bwd command")
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_R_B, GPIO.HIGH)
            I2CManager.output(I2CManager.MOTOR_L_B, GPIO.HIGH)
        reference.on_motors_started_ref(reference.get_state())


# Abstraction of turn motors command
class TurnAbcCmd(Command):

    def __init__(self):
        pass

    def execute(self, listener):
        pass


# Turn motors left command
class TurnLeftCmd(TurnAbcCmd):

    def execute(self, reference):
        print("Motor - Turning l command")
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_R_F, GPIO.HIGH)
            I2CManager.output(I2CManager.MOTOR_L_B, GPIO.HIGH)
        reference.on_motors_turning_ref(reference.get_state())


# Turn motors right command
class TurnRightCmd(TurnAbcCmd):

    def execute(self, reference):
        print("Motor - Turning r command")
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_L_F, GPIO.HIGH)
            I2CManager.output(I2CManager.MOTOR_R_B, GPIO.HIGH)
        reference.on_motors_turning_ref(reference.get_state())


# Manager of the motors.
class Motors:

    def __init__(self, on_motors_stopped_in, on_motors_started_in, on_motors_turning_in):
        print("Init  motors on %s" % py.config.CONFIG)
        self.state = MotorsState.STOP
        self.is_run = False
        self.commands = {
            MotorsState.STOP: StopCmd(),
            MotorsState.START_FWD: StartFwdCmd(),
            MotorsState.START_BWD: StartBwdCmd(),
            MotorsState.TURN_L: TurnLeftCmd(),
            MotorsState.TURN_R: TurnRightCmd(),
        }
        self.on_motors_stopped_ref = on_motors_stopped_in
        self.on_motors_started_ref = on_motors_started_in
        self.on_motors_turning_ref = on_motors_turning_in

    def start(self):
        if self.is_run:
            return
        print("Start motors")
        self.is_run = True

    def stop(self):
        if not self.is_run:
            return
        print("Stop  motors")
        self.is_run = False
        self.stop_motors()

    def on_echo(self, distance, weights):
        if not self.is_run:
            new_state = MotorsState.STOP
        else:
            new_state = self.calculate_state(weights)

        print("Motor state - new %s | current %s" % (new_state, self.get_state()))
        if new_state != self.get_state():
            self.stop_motors()
            self.set_state(new_state)

        self.exec_cmd()

    def exec_cmd(self):
        self.commands[self.get_state()].execute(self)

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def stop_motors(self):
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_R_F, GPIO.LOW)
            I2CManager.output(I2CManager.MOTOR_L_F, GPIO.LOW)
            I2CManager.output(I2CManager.MOTOR_R_B, GPIO.LOW)
            I2CManager.output(I2CManager.MOTOR_L_B, GPIO.LOW)
        self.on_motors_stopped_ref()

    def calculate_state(self, weights):
        """
        Find max move vector and decide where to go
        """
        max_idx = max(weights)
        if max_idx != 1:
            move_idx = weights.index(max_idx)
        else:
            move_idx = -1
        print("Move index is %d" % move_idx)

        if 0 <= move_idx <= 3:
            new_state = MotorsState.TURN_L
        elif 4 <= move_idx <= 7:
            new_state = MotorsState.TURN_R
        else:
            new_state = MotorsState.START_FWD

        return new_state
