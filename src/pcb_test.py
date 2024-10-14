import mcp23017_wrapper
from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
import time

# Create I2C bus object
i2c = busio.I2C(board.SCL, board.SDA)

# Create an instance of the MCP23017 class
mcpObj = MCP23017(i2c, address=0x20)

ld_ir = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 0)
ld_encoder1 = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 1)
ld_encoder2 = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 2)
ld_error = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 3)
ld_home = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 4)
ld_estop = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 9)
ls_sens = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 10)
ld_homeing = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 11)

leds = [ld_ir, ld_encoder1, ld_encoder2, ld_error, ld_home, ld_estop, ls_sens, ld_homeing]

btn_home = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 4, False)
btn_lup = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 5, False)
btn_rup = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 6, False)
btn_recalibrate = mcp23017_wrapper.MCP_CHANNEL(mcpObj, 7, False)

buttons = [btn_home, btn_lup, btn_rup, btn_recalibrate]


def test_leds():
  for led in leds:
    led.turnOn()
    time.sleep(1)
    led.turnOff()
    time.sleep(1)

def test_buttons():
  for button in buttons:
    if button.getState():
      print("Button pressed")
    else:
      print("Button not pressed")


def main():
  test_leds()

if __name__ == "__main__":
  main()

