from gpiozero import Button, OutputDevice, Device
from time import sleep
import os
from rsiStepMotor import rsiStepMotor
from mcpControl import mcpInputInterruptPin, mcpOutputPin
from rsiEncoder import rsiEncoder
from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
import threading
import time

# Define GPIO pin numbers
DIRECTION_PIN = 21
STEP_PIN = 16
ENABLE_PIN = 20
HALT_PIN = 4

# Define Encoder pins
MCP_ENCODER_A_PIN = 8
MCP_ENCODER_B_PIN = 9
INTB_PIN = 12

# Define Limit Switch pins
LEFT_INITIAL_LIMIT_SWITCH = 18
LEFT_SECONDARY_LIMIT_SWITCH = 23
RIGHT_SECONDARY_LIMIT_SWITCH = 24
RIGHT_INITIAL_LIMIT_SWITCH = 25



# Initialize GPIO devices
llsHalt = Button(LEFT_SECONDARY_LIMIT_SWITCH, pull_up=True)
rlsHalt = Button(RIGHT_SECONDARY_LIMIT_SWITCH, pull_up=True)
btnHalt = Button(HALT_PIN, pull_up=True, bounce_time=0.2)
intb_pin = Button(INTB_PIN, pull_up=True)

# Initialize I2C bus and MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)

# Initialize Encoder
encoder1 = rsiEncoder(MCP_ENCODER_A_PIN, MCP_ENCODER_B_PIN, mcp)

# Initialize Limit Switches
leftSwitch = mcpInputInterruptPin(LEFT_INITIAL_LIMIT_SWITCH, mcp)
rightSwitch = mcpInputInterruptPin(RIGHT_INITIAL_LIMIT_SWITCH, mcp)


# Initialize Motor
motor1 = rsiStepMotor(STEP_PIN, ENABLE_PIN, DIRECTION_PIN, mcp)


mcp.io_control = 0x44  # Interrupt as open drain and mirrored
mcp.clear_ints()  # Interrupts need to be cleared initially
mcp.interrupt_configuration = 0x00  # 0b00000000, compare against previous value

def haltISR(haltCode, hardExit):
	encoder1.setIRSLock(True)
	Device.close(INTB_PIN)
	motor1.haltMotor(haltCode, hardExit)

def moveUntilCondition(condition, steps, direction, speed, flag):
  while not condition():
    motor1.moveMotor(steps, direction, speed, flag)

def moveToCenter():
  motor1.moveMotor(motor1.getTrackSteps() // 2, True, 20)

def calibrateTrack():
	encoder1.setIRSLock(True)
	tempHome = 0
	tempEnd = None

	moveUntilCondition(lambda: rightSwitch.getFirstCalibration(), 1, True, 80, False)
	motor1.moveMotor(500, False, 5, False)
	rightSwitch.setLockedOut(False)

	moveUntilCondition(lambda: rightSwitch.getSecondCalibration(), 1, True, 0.001, False)
	motor1.moveMotor(20, True, 1, False)
	rightSwitch.setLockedOut(False)
	motor1.overWriteCurrentPosition(tempHome)

	moveUntilCondition(lambda: leftSwitch.getFirstCalibration(), 1, False, 80, True)
	motor1.moveMotor(500, True, 5, True)
	leftSwitch.setLockedOut(False)

	moveUntilCondition(lambda: leftSwitch.getSecondCalibration(), 1, False, 0.001, True)
	motor1.moveMotor(20, True, 1, True)
	leftSwitch.setLockedOut(False)
	tempEnd = motor1.getCurrentPosition()

	motor1.calibrateTrack(tempHome, tempEnd)
	print("Calibration Complete....")
	encoder1.setIRSLock(False)
	
def IR_RUN_STATE():
	if encoder1.isEncoderRunning():
		if motor1.isMotorMoving():
			if (time.time - encoder1.getLastTrigger()) > encoder1.getTimeout():
				encoder1.isr()
				motor1.setPower(0)
			else:
				motor1.setPower(encoder1.getSpeed())
		else:
			if motor1.getDirection():
				motor1.moveMotor(motor1.getCurrentPosition, True, 20)
			else:
				tempStepGoal = motor1.getTrackSteps() - motor1.getCurrentPosition()
				motor1.moveMotor(tempStepGoal, False, 20)
	else:
		motor1.setPower(0)  # Not sure if this is needed

def mcp_ISR():
  leftSwitch.handle_interrupt()
  rightSwitch.handle_interrupt()

intb_pin.when_pressed = mcp_ISR
llsHalt.when_pressed = lambda: haltISR("Left Emergancy Limit Switch", True)
rlsHalt.when_pressed = lambda: haltISR("Right Emergancy Limit Switch", True)
btnHalt.when_deactivated = lambda: haltISR("E-Stop Button", True)


def main():
	try:
		#calibrateTrack()
		while True:
			pass
			#IR_RUN_STATE()
	except Exception as e:
		print(f"Error: {e}")
		motor1.haltMotor("Internal Error", True)

if __name__ == "__main__":
	main()