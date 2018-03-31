import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config
from enum import Enum
from time import sleep

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO
    from py.i2c_manager import I2CManager


# Enumeration of the motors states.
class MotorsState(Enum):
    STOPPED = 1
    STARTED_FWD = 2
    STARTED_BWD = 3
    TURNING_L = 4
    TURNING_R = 5


# Manager of the motors.
class Motors:

    def __init__(self, on_motors_stopped_in, on_motors_started_in, on_motors_turning_in):
        print("Init  motors on %s" % py.config.CONFIG)
        self.min_stop_distance = 20
        self.min_start_distance = 30
        self.action_sleep = 2
        self.state = MotorsState.STOPPED
        self.is_run = False
        self.on_motors_stopped_ref = None
        self.stop_motors()
        self.on_motors_stopped_ref = on_motors_stopped_in
        self.on_motors_started_ref = on_motors_started_in
        self.on_motors_turning_ref = on_motors_turning_in

    def start(self):
        self.is_run = True
        print("Start motors")

    def stop(self):
        self.is_run = False
        print("Stop  motors")

    def on_echo(self, distance):
        print("State: %s, is run %r" % (self.state, self.is_run))
        if not self.is_run:
            self.stop_motors()
            return

        if min(distance) < self.min_stop_distance:
            if self.state is MotorsState.STOPPED:
                return
            if self.state is not (MotorsState.TURNING_L or MotorsState.TURNING_R):
                self.stop_motors()
                sleep(self.action_sleep)
            if self.is_run:
                """
                Lets turn left
                """
                self.turn_l()
        else:
            if self.state is (MotorsState.TURNING_L or MotorsState.TURNING_R):
                if min(distance) > self.min_start_distance:
                    self.stop_motors()
                    sleep(self.action_sleep)
                    if self.is_run:
                        self.forward()
                return
            if self.state is (MotorsState.STARTED_FWD or self.state is MotorsState.STARTED_BWD):
                return
            self.forward()

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