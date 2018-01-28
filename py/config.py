import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from enum import Enum


class Platform(Enum):
    LINUX = 1
    PI = 2


class Commander(Enum):
    UI = 1
    CMD = 2


# Platform configuration (Linux or Raspberry Pi)
CONFIG = Platform.LINUX
# Commander configuration (UI or Command Line(CMD))
COMMANDER = Commander.CMD
