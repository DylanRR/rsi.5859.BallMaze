import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
import time
import RPi.GPIO as GPIO

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

# Configure MCP23017 to generate interrupts on pin state changes
mcp.interrupt_enable = 0x03  # Enable interrupts on pins 8 and 9
mcp.interrupt_configuration = 0x03  # Interrupt on any change from previous state
mcp.default_value = 0x00  # Default value for comparison
mcp.interrupt_control = 0x03  # Compare against previous value

# Initialize variables
last_a = encoderA.value
last_b = encoderB.value
counter = 0
min_counter = 0
max_counter = 1000

def update_counter(channel):
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

# Setup Raspberry Pi GPIO pin for MCP23017 interrupt
interrupt_pin = 17  # GPIO pin connected to MCP23017 INT pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Attach interrupt handler to the GPIO pin
GPIO.add_event_detect(interrupt_pin, GPIO.FALLING, callback=update_counter, bouncetime=10)

try:
	print("Rotary encoder test with interrupts. Press Ctrl+C to exit.")
	while True:
		time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
	print("Exiting...")

# Clean up GPIO settings before exiting
GPIO.cleanup()