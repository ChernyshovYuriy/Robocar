import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py.ref.Adafruit_MCP230xx import Adafruit_MCP230XX


"""
Use it now as 8 output pins
"""
mcp = Adafruit_MCP230XX(address=0x20, num_gpios=8)


class I2CManager:
    """
    Manager of the I2C channel.
    """

    MOTOR_L_F = 0
    MOTOR_L_B = 1
    MOTOR_R_F = 2
    MOTOR_R_B = 3

    @staticmethod
    def init():
        # Set pins 0, 1 and 2 to output (you can set pins 0..15 this way)
        mcp.config(I2CManager.MOTOR_R_F, mcp.OUTPUT)
        mcp.config(I2CManager.MOTOR_R_B, mcp.OUTPUT)
        mcp.config(I2CManager.MOTOR_L_F, mcp.OUTPUT)
        mcp.config(I2CManager.MOTOR_L_B, mcp.OUTPUT)

    @staticmethod
    def cleanup():
        pass

    @staticmethod
    def output(pin, direction):
        mcp.output(pin, direction)

    @staticmethod
    def input(pin):
        val = (mcp.input(pin) >> pin)
        return val
