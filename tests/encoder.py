import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
import time

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP23017
mcp = MCP23017(i2c, address=0x20)

# Setup MCP23017 pins for the encoder
encoderA = mcp.get_pin(8)
encoderA.direction = Direction.INPUT
encoderA.pull = Pull.UP

encoderB = mcp.get_pin(9)
encoderB.direction = Direction.INPUT
encoderB.pull = Pull.UP

# Initialize variables
last_a = encoderA.value
last_b = encoderB.value
counter = 0
min_counter = 0
max_counter = 1000

def update_counter():
	global last_a, last_b, counter
	a = encoderA.value
	b = encoderB.value

	if a != last_a or b != last_b:
		if a == b:
			counter += 1
		else:
			counter -= 1

		# Ensure counter stays within bounds
		if counter < min_counter:
			counter = min_counter
		elif counter > max_counter:
			counter = max_counter

		print(f"Counter value: {counter}")

	last_a = a
	last_b = b

try:
	print("Rotary encoder test. Press Ctrl+C to exit.")
	while True:
		update_counter()
		time.sleep(0.01)  # Adjust the sleep time as needed
except KeyboardInterrupt:
	print("Exiting...")

# No need for GPIO cleanup as MCP23017 is handled via I2C