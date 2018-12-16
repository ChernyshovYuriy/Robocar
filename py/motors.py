import sys
import time
from os.path import dirname, abspath
from time import sleep

sys.path.append(dirname(dirname(abspath(__file__))))

from enum import Enum
import RPi.GPIO as GPIO
from py.i2c_manager import I2CManager


class MotorsState(Enum):
    """
    Enumeration of the motors states.
    """

    STOP = 1
    START_FWD = 2
    START_BWD = 3
    TURN_L = 4
    TURN_R = 5
    GO_BACK = 6
    LONG_TURN = 7


class Command:
    """
    Command interface to control motors
    """

    def execute(self, listener):
        """
        Execute single command
        :param listener: Reference to enclosing class
        :return:
        """
        raise NotImplementedError()


class StopCmd(Command):
    """
    Stop motors command.
    """

    def execute(self, reference):
        print("Motor - Stopped command")
        reference.do_stop_internal()
        reference.on_motors_stopped_ref()


class StartFwdCmd(Command):
    """
    Start motors forward command.
    """

    def execute(self, reference):
        print("Motor - Started fwd command")
        reference.do_stop_internal()
        I2CManager.output(I2CManager.MOTOR_R_F, GPIO.HIGH)
        I2CManager.output(I2CManager.MOTOR_L_F, GPIO.HIGH)
        reference.on_motors_started_ref(reference.get_state())


class StartBwdCmd(Command):
    """
    Start motors backward command.
    """

    def execute(self, reference):
        print("Motor - Started bwd command")
        reference.do_stop_internal()
        reference.do_backward_internal()
        reference.on_motors_started_ref(reference.get_state())


class GoBackCmd(Command):
    """
    Start "go back" command, in case robot stacked with wall or obstacle.
    """

    def execute(self, reference):
        print("Motor - Go back command")
        reference.do_stop_internal()
        reference.do_backward_internal()
        sleep(1)
        reference.do_left_internal()
        sleep(1)


class TurnLeftCmd(Command):
    """
    Turn motors left command.
    """

    def execute(self, reference):
        print("Motor - Turning l command")
        reference.do_stop_internal()
        reference.do_left_internal()
        reference.on_motors_turning_ref(reference.get_state())


class TurnRightCmd(Command):
    """
    Turn motors right command.
    """

    def execute(self, reference):
        print("Motor - Turning r command")
        reference.do_stop_internal()
        I2CManager.output(I2CManager.MOTOR_L_F, GPIO.HIGH)
        I2CManager.output(I2CManager.MOTOR_R_B, GPIO.HIGH)
        reference.on_motors_turning_ref(reference.get_state())


class LongTurnCmd(Command):

    def execute(self, reference):
        print("Motor - Long turn command")
        reference.do_stop_internal()
        reference.do_left_internal()
        sleep(3)


class Motors:
    """
    Manager of the motors.
    """

    RPM_MAX_FAIL_COUNT = 3
    RPM_MIN_VALUE = 10

    def __init__(self, on_motors_stopped_in, on_motors_started_in, on_motors_turning_in):
        print("Init  motors")
        self.state = MotorsState.STOP
        self.is_run = False
        self.commands = {
            MotorsState.STOP: StopCmd(),
            MotorsState.START_FWD: StartFwdCmd(),
            MotorsState.START_BWD: StartBwdCmd(),
            MotorsState.TURN_L: TurnLeftCmd(),
            MotorsState.TURN_R: TurnRightCmd(),
            MotorsState.GO_BACK: GoBackCmd(),
            MotorsState.LONG_TURN: LongTurnCmd()
        }
        self.on_motors_stopped_ref = on_motors_stopped_in
        self.on_motors_started_ref = on_motors_started_in
        self.on_motors_turning_ref = on_motors_turning_in
        self.rpm = 0
        self.rpm_fail_count = 0
        self.turn_changed_time = 0

    def start(self):
        if self.is_run:
            return
        print("Start motors")
        self.is_run = True
        self.rpm_fail_count = 0

    def stop(self):
        if not self.is_run:
            return
        print("Stop  motors")
        self.is_run = False
        self.commands[MotorsState.STOP].execute(self)

    def on_rpm(self, rpm):
        self.rpm = rpm

    def on_echo(self, distance, weights):
        state = self.calculate_state(weights)
        print("Motor state - new %s | current %s" % (state, self.get_state()))
        if state != self.get_state():
            state = self.handle_turns_changes(self.get_state(), state)
            self.set_state(state)
        self.exec_cmd()

    def exec_cmd(self):
        """
        This method introduced only for debugging purposes.
        :return:
        """
        self.commands[self.get_state()].execute(self)

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def handle_turns_changes(self, old_state, new_state):
        if (new_state == MotorsState.TURN_L or new_state == MotorsState.TURN_R) \
                and (old_state == MotorsState.TURN_L or old_state == MotorsState.TURN_R) \
                and new_state != old_state:
            if self.turn_changed_time == 0:
                self.turn_changed_time = time.time()
            if time.time() - self.turn_changed_time >= 4:
                return MotorsState.LONG_TURN
        else:
            self.turn_changed_time = 0
        return new_state

    @staticmethod
    def do_stop_internal():
        I2CManager.output(I2CManager.MOTOR_R_F, GPIO.LOW)
        I2CManager.output(I2CManager.MOTOR_L_F, GPIO.LOW)
        I2CManager.output(I2CManager.MOTOR_R_B, GPIO.LOW)
        I2CManager.output(I2CManager.MOTOR_L_B, GPIO.LOW)

    @staticmethod
    def do_backward_internal():
        I2CManager.output(I2CManager.MOTOR_R_B, GPIO.HIGH)
        I2CManager.output(I2CManager.MOTOR_L_B, GPIO.HIGH)

    @staticmethod
    def do_left_internal():
        I2CManager.output(I2CManager.MOTOR_R_F, GPIO.HIGH)
        I2CManager.output(I2CManager.MOTOR_L_B, GPIO.HIGH)

    def calculate_state(self, weights):
        """
        Calculate state of the Motors based on array of weights received from Echo module.
        :param weights: Incoming array of weights associated with distance scanned by Echo module.
        :return: MotorsState to process by the Motors command.
        """
        if not self.is_run:
            return MotorsState.STOP

        if weights[3] < 1:
            return MotorsState.STOP
        """
        Find max move vector and decide where to go.
        //TODO: Check whether peaks are on both sides of vector (in 1 or 2 and in 4 or 5) - potential corner
                Overall, not a best solution ...
        """
        max_idx = max(weights)
        """
        Assume if max is 1 then all weights are equals, means no abstraction detected.
        """
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

        """
        In case of vehicle stacked forward, for instance hit the wall, do back up move.
        //TODO: Use gyro to track stack in case of turn
        """
        if new_state == MotorsState.START_FWD:
            print("::TRACE::%d %d" % (self.rpm_fail_count, self.rpm))
            if self.rpm <= Motors.RPM_MIN_VALUE:
                if self.rpm_fail_count >= Motors.RPM_MAX_FAIL_COUNT:
                    new_state = MotorsState.GO_BACK
                    self.rpm_fail_count = 0
                else:
                    self.rpm_fail_count += 1
            else:
                self.rpm_fail_count = 0

        """
        This is the case when robot drive near a wall almost parallel. If all sensors are 1 except any left most
        or right most - move forward
        """
        if new_state == MotorsState.TURN_L or new_state == MotorsState.TURN_R:
            if weights[1] == 1 and weights[2] == 1 and weights[3] == 1 and weights[4] == 1 and weights[5] == 1:
                new_state = MotorsState.START_FWD

        return new_state
