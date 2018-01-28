import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from enum import Enum


# Enumeration of the available platforms supported
class Platform(Enum):
    LINUX = 1
    PI = 2


# Enumeration of the commanders supported. UI - based on TKinter. CMD - command line.
class Commander(Enum):
    UI = 1
    CMD = 2


# Current platform configuration (Linux or Raspberry Pi)
CONFIG = Platform.LINUX
# Current commander configuration (UI or Command Line(CMD))
COMMANDER = Commander.CMD
