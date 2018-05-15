import sys
from os.path import dirname, abspath
from time import sleep

sys.path.append(dirname(dirname(abspath(__file__))))

from py.lm393 import LM393_MAX_COUNTER
import py.config
from enum import Enum

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO
    from py.i2c_manager import I2CManager

# 8inch 20cm
min_stop_distance = 8
# 12inch 30cm
min_start_distance = 12
TURN_SLEEP = 0.1


# Enumeration of the motors states.
class MotorsState(Enum):
    STOPPED = 1
    STARTED_FWD = 2
    STARTED_BWD = 3
    TURNING_L = 4
    TURNING_R = 5
    HIT_THE_WALL = 6


# Interface
class Command:

    def execute(self, state, distance, listener):
        raise NotImplementedError()


# Stopped command
class StoppedCmd(Command):

    def execute(self, state, distance, listener):
        print("Motor - Stopped command")
        if min(distance) >= min_stop_distance:
            listener.forward()
            return
        if distance[0] < min_stop_distance:
            listener.turn_r()
        elif distance[len(distance) - 1] < min_stop_distance:
            listener.turn_l()
        else:
            listener.turn_l()


# Started fwd command
class StartedFwdCmd(Command):

    def execute(self, state, distance, listener):
        print("Motor - Started fwd command")
        if min(distance) >= min_stop_distance:
            listener.handle_lm393()
            return
        listener.stop_motors()


# Started bwd command
class StartedBwdCmd(Command):

    def execute(self, state, distance, listener):
        print("Motor - Started bwd command")


# Turning l command
class TurningLCmd(Command):

    def execute(self, state, distance, listener):
        print("Motor - Turning l command")
        if min(distance) >= min_stop_distance:
            sleep(TURN_SLEEP)
            listener.stop_motors()
        else:
            # listener.handle_lm393()
            pass


# Turning r command
class TurningRCmd(Command):

    def execute(self, state, distance, listener):
        print("Motor - Turning r command")
        if min(distance) >= min_stop_distance:
            sleep(TURN_SLEEP)
            listener.stop_motors()
        else:
            # listener.handle_lm393()
            pass


# Hit the wall command
class HitTheWallCmd(Command):

    def execute(self, state, distance, listener):
        print("Motor - Hit the wall command")
        listener.stop_motors()
        listener.backward()
        sleep(1)
        listener.turn_l()


# Manager of the motors.
class Motors:

    def __init__(self, on_motors_stopped_in, on_motors_started_in, on_motors_turning_in):
        print("Init  motors on %s" % py.config.CONFIG)
        self.state = MotorsState.STOPPED
        self.is_run = False
        self.on_motors_stopped_ref = None
        self.lm393_value = 0
        self.commands = {MotorsState.STOPPED: StoppedCmd(),
                         MotorsState.STARTED_FWD: StartedFwdCmd(),
                         MotorsState.STARTED_BWD: StartedBwdCmd(),
                         MotorsState.TURNING_L: TurningLCmd(),
                         MotorsState.TURNING_R: TurningRCmd(),
                         MotorsState.HIT_THE_WALL: HitTheWallCmd()}
        self.stop_motors()
        self.on_motors_stopped_ref = on_motors_stopped_in
        self.on_motors_started_ref = on_motors_started_in
        self.on_motors_turning_ref = on_motors_turning_in
        self.zero_counter = 0

    def set_lm393_value(self, value):
        self.lm393_value = value

    def start(self):
        self.is_run = True
        print("Start motors")

    def stop(self):
        self.is_run = False
        print("Stop  motors")

    def on_echo(self, distance):
        print("State: %s, is run %r, lm393 %d" % (self.state, self.is_run, self.lm393_value))

        if not self.is_run:
            self.stop_motors()
            return

        self.commands[self.state].execute(self.state, distance, self)

    def forward(self):
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_R_F, GPIO.HIGH)
            I2CManager.output(I2CManager.MOTOR_L_F, GPIO.HIGH)
        self.state = MotorsState.STARTED_FWD
        self.on_motors_started_ref(self.state)

    def backward(self):
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_R_B, GPIO.HIGH)
            I2CManager.output(I2CManager.MOTOR_L_B, GPIO.HIGH)
        self.state = MotorsState.STARTED_BWD
        self.on_motors_started_ref(self.state)

    def stop_motors(self):
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_R_F, GPIO.LOW)
            I2CManager.output(I2CManager.MOTOR_L_F, GPIO.LOW)
            I2CManager.output(I2CManager.MOTOR_R_B, GPIO.LOW)
            I2CManager.output(I2CManager.MOTOR_L_B, GPIO.LOW)
        self.state = MotorsState.STOPPED
        if self.on_motors_stopped_ref is not None:
            self.on_motors_stopped_ref()

    def turn_l(self):
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_R_F, GPIO.HIGH)
            I2CManager.output(I2CManager.MOTOR_L_B, GPIO.HIGH)
        self.state = MotorsState.TURNING_L
        self.on_motors_turning_ref(self.state)

    def turn_r(self):
        if py.config.CONFIG is py.config.Platform.PI:
            I2CManager.output(I2CManager.MOTOR_L_F, GPIO.HIGH)
            I2CManager.output(I2CManager.MOTOR_R_B, GPIO.HIGH)
        self.state = MotorsState.TURNING_R
        self.on_motors_turning_ref(self.state)

    def hit_the_wall(self):
        self.state = MotorsState.HIT_THE_WALL

    def handle_lm393(self):
        if self.lm393_value <= 0 or self.lm393_value == LM393_MAX_COUNTER:
            self.zero_counter += 1
            if self.zero_counter == 10:
                self.zero_counter = 0
                self.hit_the_wall()
        else:
            self.zero_counter = 0
