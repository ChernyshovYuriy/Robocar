import sys
from os.path import dirname, abspath

from py.Adafruit_GPIO.MCP230xx import MCP23017

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config

if py.config.CONFIG is py.config.Platform.PI:
    from py.Adafruit_MCP230xx import Adafruit_MCP230XX


if py.config.CONFIG is py.config.Platform.PI:
    mcp = MCP23017()


# Manager of the I2C channel.
class I2CManager:

    TRIGGER_2 = 8
    ECHO_2 = 0

    @staticmethod
    def init():
        if py.config.CONFIG is py.config.Platform.PI:
            # Set pins 0, 1 and 2 to output (you can set pins 0..15 this way)
            mcp.setup(I2CManager.TRIGGER_2, mcp.OUTPUT)
            mcp.setup(I2CManager.ECHO_2, mcp.INPUT)
            mcp.pullup(I2CManager.ECHO_2, 1)

    @staticmethod
    def cleanup():
        if py.config.CONFIG is py.config.Platform.PI:
            pass

    @staticmethod
    def output(pin, direction):
        mcp.output(pin, direction)

    @staticmethod
    def input(pin):
        val = (mcp.input(pin) >> pin)
        print("VAL:%f" % val)
        return val
