import sys
from os.path import dirname, abspath
from time import sleep, time

sys.path.append(dirname(dirname(abspath(__file__))))

from py.lm393 import LM393_MAX_COUNTER
import py.config
from enum import Enum

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO
    from py.i2c_manager import I2CManager

# 8inch 20cm
MIN_STOP_DISTANCE = 12
# 12inch 30cm
MIN_START_DISTANCE = 12
TURN_SLEEP = 0.1


# Enumeration of the motors states.
class MotorsState(Enum):
    STOPPED = 1
    STARTED_FWD = 2
    STARTED_BWD = 3
    TURNING_L = 4
    TURNING_R = 5


# Interface
class Command:

    def execute(self, state, distance, listener):
        raise NotImplementedError()


# Stopped command
class StoppedCmd(Command):

    def execute(self, state, distance, listener):
        print("Motor - Stopped command")
        if listener.is_run:
            listener.make_move_decision(distance)


# Started fwd command
class StartedFwdCmd(Command):

    def execute(self, state, distance, listener):
        print("Motor - Started fwd command")
        if min(distance) >= MIN_STOP_DISTANCE:
            # listener.handle_lm393()
            return
        listener.stop_motors()
        listener.make_move_decision(distance)


# Started bwd command
class StartedBwdCmd(Command):

    def execute(self, state, distance, listener):
        print("Motor - Started bwd command")


class TurningAbcCmd(Command):

    def __init__(self):
        self.lm393_value = 0
        self.zero_counter = 0
        self.escape_forward = True

    def execute(self, state, distance, listener):
        print("Motor - Turning abc command")
        if self.lm393_value <= 0 or self.lm393_value == LM393_MAX_COUNTER:
            self.zero_counter += 1
            if self.zero_counter == 10:
                self.zero_counter = 0
                if self.escape_forward:
                    listener.stop_motors()
                    listener.forward()
                    self.escape_forward = False
                else:
                    listener.stop_motors()
                    listener.backward()
                    sleep(2)
                    listener.forward()
                    self.escape_forward = True
        else:
            self.zero_counter = 0
        pass


# Turning l command
class TurningLCmd(TurningAbcCmd):

    def execute(self, state, distance, listener):
        print("Motor - Turning l command")
        if min(distance) >= MIN_STOP_DISTANCE:
            # sleep(TURN_SLEEP)
            listener.stop_motors()
            listener.make_move_decision(distance)
        else:
            # super().execute(state, distance, listener)
            pass


# Turning r command
class TurningRCmd(TurningAbcCmd):

    def execute(self, state, distance, listener):
        print("Motor - Turning r command")
        if min(distance) >= MIN_STOP_DISTANCE:
            # sleep(TURN_SLEEP)
            listener.stop_motors()
            listener.make_move_decision(distance)
        else:
            # super().execute(state, distance, listener)
            pass


# Manager of the motors.
class Motors:

    def __init__(self, on_motors_stopped_in, on_motors_started_in, on_motors_turning_in):
        print("Init  motors on %s" % py.config.CONFIG)
        self.state = MotorsState.STOPPED
        self.is_run = False
        self.on_motors_stopped_ref = None
        self.lm393_value = 0
        self.commands = {
            MotorsState.STOPPED: StoppedCmd(),
            MotorsState.STARTED_FWD: StartedFwdCmd(),
            MotorsState.STARTED_BWD: StartedBwdCmd(),
            MotorsState.TURNING_L: TurningLCmd(),
            MotorsState.TURNING_R: TurningRCmd(),
        }
        self.stop_motors()
        self.on_motors_stopped_ref = on_motors_stopped_in
        self.on_motors_started_ref = on_motors_started_in
        self.on_motors_turning_ref = on_motors_turning_in
        self.zero_counter = 0
        self.turn_l_counter = 0
        self.turn_r_counter = 0
        self.turn_start = 0

    def set_lm393_value(self, value):
        self.lm393_value = value

    def start(self):
        self.is_run = True
        print("Start motors")
        self.forward()

    def stop(self):
        self.is_run = False
        print("Stop  motors")
        self.stop_motors()

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

    # def handle_lm393(self):
    #     if self.lm393_value <= 0 or self.lm393_value == LM393_MAX_COUNTER:
    #         self.zero_counter += 1
    #         if self.zero_counter == 10:
    #             self.zero_counter = 0
    #     else:
    #         self.zero_counter = 0

    def make_move_decision(self, distance):
        if min(distance) >= MIN_STOP_DISTANCE:
            self.forward()
            self.turn_l_counter = 0
            self.turn_r_counter = 0
            self.turn_start = 0
            return

        timestamp = time()
        if self.turn_start is 0:
            self.turn_start = timestamp
        # print("Timestamp %d, turn start %d, diff %d" % (timestamp, self.turn_start, (timestamp - self.turn_start)))
        if timestamp - self.turn_start >= 3:
            self.turn_l()
            sleep(1)
            return

        if distance[0] < MIN_STOP_DISTANCE:
            self.turn_r()
            self.turn_r_counter += 1
            sleep(TURN_SLEEP)
            self.stop_motors()
        elif distance[len(distance) - 1] < MIN_STOP_DISTANCE:
            self.turn_l()
            self.turn_l_counter += 1
            sleep(TURN_SLEEP)
            self.stop_motors()
        else:
            self.turn_l()
            self.turn_l_counter += 1
            sleep(TURN_SLEEP)
            self.stop_motors()