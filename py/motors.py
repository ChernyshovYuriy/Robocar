import sys
from enum import Enum
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config


class MotorsState(Enum):
    STOPPED = 1
    STARTED = 2


class Motors:

    min_stop_distance = 10
    min_start_distance = 50

    def __init__(self, on_motors_stopped_in, on_motors_started_in):
        print("Init  motors on %s" % py.config.CONFIG)
        self.state = MotorsState.STOPPED
        self.on_motors_stopped_ref = on_motors_stopped_in
        self.on_motors_started_ref = on_motors_started_in

    def on_echo(self, distance):
        # print("Distance: %d" % distance)
        if distance < Motors.min_stop_distance:
            if self.state is MotorsState.STOPPED:
                return
            self.state = MotorsState.STOPPED
            self.on_motors_stopped_ref()
        else:
            if self.state is MotorsState.STARTED:
                return
            self.state = MotorsState.STARTED
            self.on_motors_started_ref()