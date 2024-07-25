from gpiozero import Button, OutputDevice, Device
from time import sleep
import os
from rsiStepMotor import rsiStepMotor

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
lls = Button(LEFT_INITIAL_LIMIT_SWITCH, pull_up=True)
rls = Button(RIGHT_INITIAL_LIMIT_SWITCH, pull_up=True)
intb_pin = Button(INTB_PIN, pull_up=True)

# Initialize I2C bus and MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)

# Initialize Motor
motor1 = rsiStepMotor(STEP_PIN, DIRECTION_PIN, ENABLE_PIN, mcp)

# Initialize Encoder
encoder1 = rsiEncoder(MCP_ENCODER_A_PIN, MCP_ENCODER_B_PIN, mcp)


rlsFirstCalibration = False
rlsSecondCalibration = False
rlsLockOut = False
def right_ls():
	global rlsFirstCalibration, rlsSecondCalibration, rlsLockOut
	if rlsLockOut:
		return
	encoder1.setIRSLock(True)
	
	if not rlsFirstCalibration:
		rlsFirstCalibration = True
		rlsLockOut = True
		return
	
	if not rlsSecondCalibration:
		rlsSecondCalibration = True
		rlsLockOut = True
		return
	encoder1.setIRSLock(False)


llsFirstCalibration = False
llsSecondCalibration = False
llsLockOut = False
def left_ls():
	global llsFirstCalibration, llsSecondCalibration, llsLockOut
	if llsLockOut:
		return
	encoder1.setIRSLock(True)
	
	if not llsFirstCalibration:
		llsFirstCalibration = True
		llsLockOut = True
		return
	
	if not llsSecondCalibration:
		llsSecondCalibration = True
		llsLockOut = True
		return
	encoder1.setIRSLock(False)

def moveUntilCondition(condition, steps, direction, speed, flag):
    while not condition():
        motor1.moveMotor(steps, direction, speed, flag)

def calibrateTrack():
	encoder1.setIRSLock(True)
	global rlsFirstCalibration, rlsSecondCalibration, rlsLockOut, llsFirstCalibration, llsSecondCalibration, llsLockOut
	rlsFirstCalibration = False
	rlsSecondCalibration = False
	rlsLockOut = False
	llsFirstCalibration = False
	llsSecondCalibration = False
	llsLockOut = False
	tempHome = 0
	tempEnd = None

	moveUntilCondition(lambda: rlsFirstCalibration, 1, True, 80, False)
	motor1.moveMotor(500, False, 5, False)
	rlsLockOut = False

	moveUntilCondition(lambda: rlsSecondCalibration, 1, True, 0.001, False)
	motor1.moveMotor(20, True, 1, False)
	rlsLockOut = False
	motor1.overWriteCurrentPosition(tempHome)

	moveUntilCondition(lambda: llsFirstCalibration, 1, False, 80, True)
	motor1.moveMotor(500, True, 5, True)
	llsLockOut = False

	moveUntilCondition(lambda: llsSecondCalibration, 1, False, 0.001, True)
	motor1.moveMotor(20, True, 1, True)
	llsLockOut = False
	tempEnd = motor1.getCurrentPosition()

	motor1.calibrateTrack(tempHome, tempEnd)
	print("Calibration Complete....")
	encoder1.setIRSLock(False)

def initializeEncoderInterrupts():
	mcp.interrupt_enable = 0xFFFF
	mcp.interrupt_configuration = 0x0000  # interrupt on any change
	mcp.io_control = 0x44  # Interrupt as open drain and mirrored
	mcp.clear_ints()  # Interrupts need to be cleared initially
	# Configure interrupts to trigger on a change
	mcp.interrupt_configuration = 0x00  # 0b00000000, compare against previous value


def encoderISR():
	threading.Thread(target=encoder1.isr).start()
	

def haltISR(haltCode, hardExit):
	encoder1.setIRSLock(True)
	Device.close(INTB_PIN)
	motor1.haltMotor(haltCode, hardExit)


def IR_RUN_STATE():
	print("IR_RUN_STATE")
	if not encoder1.isEncoderRunning():
		return
	
	direction = encoder1.getDirection()
	speed = encoder1.getSpeed()
	position = motor1.getCurrentPosition()
	step_goal = None
	if direction:
		step_goal = position - motor1.getHomePosition()
	else:
		step_goal = motor1.getEndPosition() - position
	
	motor1.moveMotor(step_goal, direction, speed)
	while encoder1.isEncoderRunning():
		motor1.setPower(encoder1.getSpeed())
		last_trigger_time = encoder1.getLastTrigger()

		tempTime = (time.time() - last_trigger_time) * 1000
		if tempTime > encoder1.getTimeout():
			encoder1.isr()

	motor1.setPower(0)


#Setting Interrupts
llsHalt.when_pressed = lambda: haltISR("Left Emergancy Limit Switch", True)
rlsHalt.when_pressed = lambda: haltISR("Right Emergancy Limit Switch", True)
btnHalt.when_deactivated = lambda: haltISR("E-Stop Button", True)
lls.when_pressed = left_ls
rls.when_pressed = right_ls
intb_pin.when_pressed = encoderISR

def main():
	try:
		calibrateTrack()
		sleep(3)
		steps2Mid = round(motor1.getEndPosition() / 2) 
		motor1.moveMotor(steps2Mid, True, 80, True)
		sleep(3)
		while True:
			IR_RUN_STATE()
	except Exception as e:
		print(f"Error: {e}")
		motor1.haltMotor("Internal Error", True)


if __name__ == "__main__":
	main()
