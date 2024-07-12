from gpiozero import Button
from signal import pause
import busio
import board
from adafruit_mcp230xx.mcp23017 import MCP23017
from digitalio import Direction, Pull

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

# Setup GPIO pin for MCP23017 interrupt (using GPIO Zero)
interrupt_pin = Button(12)  # Assuming the MCP23017 interrupt is connected to GPIO 4

position = 0
last_state = None

def encoder_interrupt():
	global position, last_state
	state_a = encoderA.value
	state_b = encoderB.value
	current_state = (state_a, state_b)
	
	if current_state != last_state:
		if last_state is not None:
			if last_state == (0, 1) and current_state == (1, 1):
				position += 1
			elif last_state == (1, 0) and current_state == (1, 1):
				position -= 1
		last_state = current_state
	print(f"Position: {position}")

# Attach the interrupt handler
interrupt_pin.when_pressed = encoder_interrupt

pause()  # Wait indefinitely for interrupts