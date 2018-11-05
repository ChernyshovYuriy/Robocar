import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config
from enum import Enum

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO
    from py.i2c_manager import I2CManager

# 8inch 20cm
# 12inch 30cm
MIN_STOP_DISTANCE = 10
MIN_START_DISTANCE = 10
TURN_SLEEP = 0.3
TURN_FAIL_COUNTER = 5


# Enumeration of the motors states.
class MotorsState(Enum):
    STOP = 1
    START_FWD = 2
    STAR_BWD = 3
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
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_R_F, GPIO.LOW)
            I2CManager.output(I2CManager.MOTOR_L_F, GPIO.LOW)
            I2CManager.output(I2CManager.MOTOR_R_B, GPIO.LOW)
            I2CManager.output(I2CManager.MOTOR_L_B, GPIO.LOW)
        reference.on_motors_stopped_ref()


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
            MotorsState.STAR_BWD: StartBwdCmd(),
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

    def on_echo(self, distance):
        print("State: %s, is run: %r, distance: %s" % (self.get_state(), self.is_run, distance))

        # TODO: Make decision about state based on array of distances and is_run

        self.exec_cmd()

    def exec_cmd(self):
        self.commands[self.get_state()].execute(self)

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state
