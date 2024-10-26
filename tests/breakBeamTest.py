import board
import busio
import time
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP23017
mcp = MCP23017(i2c, address=0x20)

# Configure pin 8 as an input
breakBeam_pin = mcp.get_pin(8)
breakBeam_pin.switch_to_input(pull=digitalio.Pull.UP)

while True:
    # Read the value of pin 8
    pin_value = breakBeam_pin.value
    print(f"Pin 8 value: {pin_value}")
    time.sleep(0.1)
