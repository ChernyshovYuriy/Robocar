import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config
from enum import Enum
from time import sleep
from py.gpio_manager import GPIOManager

if py.config.CONFIG is py.config.Platform.PI:
    import RPi.GPIO as GPIO


# Enumeration of the motors states.
class MotorsState(Enum):
    STOPPED = 1
    STARTED_FWD = 2
    STARTED_BWD = 3
    TURNING = 4


# Manager of the motors.
class Motors:

    def __init__(self, on_motors_stopped_in, on_motors_started_in, on_motors_turning_in):
        print("Init  motors on %s" % py.config.CONFIG)
        self.min_stop_distance = 10
        self.min_start_distance = 10
        self.action_sleep = 2
        self.state = MotorsState.STOPPED
        self.is_run = False
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
        # print("Distance: %d, state: %s" % (distance, self.state))
        if not self.is_run:
            self.stop_motors()
            return

        if distance < self.min_stop_distance:
            if self.state is MotorsState.STOPPED:
                return
            self.stop_motors()
            sleep(self.action_sleep)
            if self.is_run:
                self.turn()
        else:
            if self.state is MotorsState.TURNING:
                if distance > self.min_start_distance:
                    self.stop_motors()
                    sleep(self.action_sleep)
                    if self.is_run:
                        self.forward()
                return
            if self.state is MotorsState.STARTED_FWD or self.state is MotorsState.STARTED_BWD:
                return
            self.forward()

    def forward(self):
        if py.config.CONFIG is py.config.Platform.PI:
            print("Forward ->")
            GPIO.output(GPIOManager.MOTOR_R_F, GPIO.HIGH)
            GPIO.output(GPIOManager.MOTOR_L_F, GPIO.HIGH)
        self.state = MotorsState.STARTED_FWD
        self.on_motors_started_ref(self.state)

    def backward(self):
        if py.config.CONFIG is py.config.Platform.PI:
            print("Backward ->")
            GPIO.output(GPIOManager.MOTOR_R_B, GPIO.HIGH)
            GPIO.output(GPIOManager.MOTOR_L_B, GPIO.HIGH)
        self.state = MotorsState.STARTED_BWD
        self.on_motors_started_ref(self.state)

    def stop_motors(self):
        if py.config.CONFIG is py.config.Platform.PI:
            print("Stop ->")
            GPIO.output(GPIOManager.MOTOR_R_F, GPIO.LOW)
            GPIO.output(GPIOManager.MOTOR_L_F, GPIO.LOW)
            GPIO.output(GPIOManager.MOTOR_R_B, GPIO.LOW)
            GPIO.output(GPIOManager.MOTOR_L_B, GPIO.LOW)
        self.state = MotorsState.STOPPED
        self.on_motors_stopped_ref()

    def turn(self):
        if py.config.CONFIG is py.config.Platform.PI:
            GPIO.output(GPIOManager.MOTOR_R_F, GPIO.HIGH)
            GPIO.output(GPIOManager.MOTOR_L_B, GPIO.HIGH)
        self.state = MotorsState.TURNING
        self.on_motors_turning_ref()