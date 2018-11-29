import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from enum import Enum


# Enumeration of the commanders supported. UI - based on TKinter. CMD - command line.
class Commander(Enum):
    UI = 1
    CMD = 2


# Current commander configuration (UI or Command Line(CMD))
COMMANDER = Commander.CMD
