from rsiStepMotor import rsiStepMotor
from time import sleep
from gpiozero import Button
from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from encoderv2 import Encoder

# Define GPIO pin numbers
DIRECTION_PIN = 6 # MCP Pin
STEP_PIN = 16			# Pi Pin     
ENABLE_PIN = 7		# MCP Pin
HALT_PIN = 4			# Pi Pin

# Define Encoder pins
ENCODER_A_PIN = 5	# Pi Pin
ENCODER_B_PIN = 6	# Pi Pin
INTA_PIN = 12			# Pi Pin

# Define Limit Switch pins
LEFT_INITIAL_LIMIT_SWITCH = 5			# MCP Pin
LEFT_SECONDARY_LIMIT_SWITCH = 23	# Pi Pin
RIGHT_SECONDARY_LIMIT_SWITCH = 24	# Pi Pin
RIGHT_INITIAL_LIMIT_SWITCH = 4		# MCP Pin


# Initialize I2C bus and MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)

motor1 = rsiStepMotor(STEP_PIN, DIRECTION_PIN, ENABLE_PIN, mcp)

# Initialize GPIO devices
llsHalt = Button(LEFT_SECONDARY_LIMIT_SWITCH, pull_up=True)
rlsHalt = Button(RIGHT_SECONDARY_LIMIT_SWITCH, pull_up=True)
btnHalt = Button(HALT_PIN, pull_up=True, bounce_time=0.2)
intA_pin = Button(INTA_PIN)

# Initialize Encoder
encoder1 = Encoder(ENCODER_A_PIN, ENCODER_B_PIN)


def moveTest():
	motor1.enableMotor()
	motor1.moveMotor(6000, False, 5)
	motor1.disableMotor()


btnHalt.when_deactivated = lambda: motor1.haltMotor("E-Stop Button", True)

def main():
	try:
		while True:
			print(f"Encoder Direction: {encoder1.direction}")
			print(f"Encoder Value: {encoder1.getSpeed()}")
			sleep(1)
		moveTest()
	except Exception as e:
		print(f"Error: {e}")
	finally:
		motor1.haltMotor("Program Complete", True)


if __name__ == "__main__":
	main()