from rsiStepMotor import rsiStepMotor
from time import sleep
from gpiozero import Button
from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio

DIRECTION_PIN = 6
STEP_PIN = 16
ENABLE_PIN = 7
HALT_PIN = 4

# Initialize I2C bus and MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)

motor1 = rsiStepMotor(STEP_PIN, DIRECTION_PIN, ENABLE_PIN, mcp)
btnHalt = Button(HALT_PIN, pull_up=True, bounce_time=0.2)

def enableDisableTest():
	motor1.enableMotor()
	print("Motor Enabled")
	sleep(5)
	motor1.disableMotor()
	print("Motor Disabled")
	
def setDirectionTest():
	motor1.setDirection(True)
	print("Motor set to clockwise")
	sleep(5)
	motor1.setDirection(False)
	print("Motor set to counter-clockwise")

def setPowerTest():
	print("Setting power NO RAMP")
	motor1.setPower(5, False)
	print("Power set with no ramp success")
	sleep(5)
	print("Setting power WITH RAMP under 10%")
	motor1.setPower(7, True)
	print("Power set with ramp under 10 success")
	sleep(5)
	print("Setting power WITH RAMP over 10%")
	motor1.setPower(50, True)
	print("Power set with ramp over 10 success")

def moveTest():
	motor1.enableMotor()
	motor1.moveMotor(4000, True, 10)
	motor1.disableMotor()


btnHalt.when_deactivated = lambda: motor1.haltMotor("E-Stop Button", True)
def main():
	try:
		#enableDisableTest()
		#setDirectionTest()
		#moveTest()
		setPowerTest()
		#moveTest()
	except Exception as e:
		print(f"Error: {e}")
	finally:
		motor1.haltMotor("Program Complete", True)


if __name__ == "__main__":
	main()