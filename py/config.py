import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from enum import Enum


class Platform(Enum):
    LINUX = 1
    PI = 2


# Platform configuration (Linux or Raspberry Pi)
CONFIG = Platform.LINUX
