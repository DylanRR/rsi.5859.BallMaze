from gpiozero import Button, OutputDevice, Device
from time import sleep
from rsiStepMotor import rsiStepMotor
from mcpControl import mcpInputInterruptPin, mcpOutputPin
from encoderv2 import Encoder
from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio

# Define GPIO pin numbers
DIRECTION_PIN = 6 # MCP Pin    Was 7
STEP_PIN = 16			# Pi Pin     
ENABLE_PIN = 7		# MCP Pin		 Was 6
HALT_PIN = 4			# Pi Pin

# Define Encoder pins
MCP_ENCODER_A_PIN = 5	# Pi Pin
MCP_ENCODER_B_PIN = 6	# Pi Pin
INTA_PIN = 12					# Pi Pin

# Define Limit Switch pins
LEFT_INITIAL_LIMIT_SWITCH = 5			# MCP Pin
LEFT_SECONDARY_LIMIT_SWITCH = 23	# Pi Pin
RIGHT_SECONDARY_LIMIT_SWITCH = 24	# Pi Pin
RIGHT_INITIAL_LIMIT_SWITCH = 4		# MCP Pin



# Initialize GPIO devices
llsHalt = Button(LEFT_SECONDARY_LIMIT_SWITCH, pull_up=True)
rlsHalt = Button(RIGHT_SECONDARY_LIMIT_SWITCH, pull_up=True)
btnHalt = Button(HALT_PIN, pull_up=True, bounce_time=0.2)
intA_pin = Button(INTA_PIN)

# Initialize I2C bus and MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)

# Initialize Encoder
encoder1 = Encoder(MCP_ENCODER_A_PIN, MCP_ENCODER_B_PIN)

# Initialize Limit Switches
leftSwitch = mcpInputInterruptPin(LEFT_INITIAL_LIMIT_SWITCH, mcp)
rightSwitch = mcpInputInterruptPin(RIGHT_INITIAL_LIMIT_SWITCH, mcp)


# Initialize Motor
motor1 = rsiStepMotor(STEP_PIN, DIRECTION_PIN, ENABLE_PIN, mcp) # <------------------------------IM DUMB

mcp.clear_ints()  # Interrupts need to be cleared initially
mcp.interrupt_configuration = 0x00  # 0b00000000, compare against previous value

def haltISR(haltCode, hardExit):
	encoder1.ISR_LOCK(True)
	Device.close(INTA_PIN)
	motor1.haltMotor(haltCode, hardExit)

def moveUntilCondition(condition, steps, direction, speed, trackPos=True, rampOverride=False):
  while not condition():
    motor1.moveMotor(steps, direction, speed, trackPos, rampOverride)

def moveToCenter():
	print("Moving to Center")
	motor1.moveMotor(motor1.getTrackSteps() // 2, True, 20)

def calibrateTrack():
	print("Entered Calibration Mode....")
	encoder1.ISR_LOCK(True)
	print("Encoder Locked")
	tempHome = 0
	tempEnd = None

	motor1.enableMotor()
	leftSwitch.setLockedOut(True)
	moveUntilCondition(lambda: rightSwitch.getFirstCalibration(), 1, True, 60, False)
	motor1.moveMotor(500, False, 5, False)
	rightSwitch.setLockedOut(False)

	moveUntilCondition(lambda: rightSwitch.getSecondCalibration(), 1, True, 0.001, False,)
	motor1.moveMotor(20, True, 1, False)
	rightSwitch.setLockedOut(False)
	motor1.overWriteCurrentPosition(tempHome)

	leftSwitch.setLockedOut(False)
	moveUntilCondition(lambda: leftSwitch.getFirstCalibration(), 1, False, 60, True)
	motor1.moveMotor(500, True, 5, True)
	leftSwitch.setLockedOut(False)

	moveUntilCondition(lambda: leftSwitch.getSecondCalibration(), 1, False, 0.001, True)
	motor1.moveMotor(20, True, 1, True)
	leftSwitch.setLockedOut(False)
	tempEnd = motor1.getCurrentPosition()

	motor1.calibrateTrack(tempHome, tempEnd)
	moveToCenter()
	print("Calibration Complete....")
	encoder1.ISR_LOCK(False)


def moveUntilConditionUpdating(condition, steps, direction, speed, trackPos=True, rampOverride=False):
  while not condition():
    motor1.moveMotor(steps, direction, speed, trackPos, rampOverride)

def dirChange():
	if motor1.getDirection():
		tempPos = motor1.getCurrentPosition()
		motor1.moveMotor(tempPos, True, 20)    #<----- We need to use a moveUntil taking 1 step at a time and checking for encoder direction change / speed each step
	else:
		tempStepGoal = motor1.getTrackSteps() - motor1.getCurrentPosition()
		motor1.moveMotor(tempStepGoal, False, 20)

def mMoveNoDirChange():
	tSpeed = encoder1.getSpeed()
	if not tSpeed == 0:
		motor1.setPower(encoder1.getSpeed())

lastKnownDir = None
def IR_RUN_STATE():
	global lastKnownDir
	if encoder1.isEncoderRunning():
		if motor1.isMotorMoving():
			if not encoder1.hasDirChanged(lastKnownDir):
				mMoveNoDirChange()
			else:
				motor1.setPower(0)  # Not sure if this is needed
				dirChange()
		else:
			dirChange()
	else:
		motor1.setPower(0)  # Not sure if this is needed

def mcp_ISR():
	initFlagA = mcp.int_flaga
	if not initFlagA:
		return
	print("-------------------Interrupt detected-------------------")
	print(f"MCP Interrupt Flag List: {initFlagA}")

	#print(f"Flag at 0: {initFlagA[0]}")
	#print(f"INFO:Left Switch Pin: {leftSwitch.pin}")
	#print(f"INFO:Right Switch Pin: {rightSwitch.pin}")
	
	if initFlagA[0] == leftSwitch.pin:
		print("Handling left switch interrupt (Pin 5)")
		leftSwitch.handle_interrupt()
	elif initFlagA[0] == rightSwitch.pin:
		print("Handling right switch interrupt (pin 4)")
		rightSwitch.handle_interrupt()
	else:
		print("No matching interrupt handler found")

	mcp.clear_inta()
	print("Interrupt flags cleared")

intA_pin.when_pressed = mcp_ISR
llsHalt.when_pressed = lambda: haltISR("Left Emergancy Limit Switch", True)
rlsHalt.when_pressed = lambda: haltISR("Right Emergancy Limit Switch", True)
btnHalt.when_deactivated = lambda: haltISR("E-Stop Button", True)

def main():
	try:
		calibrateTrack()
		while True:
			#break
			IR_RUN_STATE()
	except Exception as e:
		print(f"Error: {e}")
		motor1.haltMotor("Internal Error", True)
	finally:
		motor1.haltMotor("Program Complete", True)


def main():
	calibrateTrack()
	while True:
		IR_RUN_STATE()

if __name__ == "__main__":
	main()