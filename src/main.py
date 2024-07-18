from gpiozero import Button, OutputDevice
from time import sleep
import os
from rsiStepMotor import rsiStepMotor

# Define GPIO pin numbers
DIRECTION_PIN = 21
STEP_PIN = 16
ENABLE_PIN = 20
HALT_PIN = 4

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

# Initialize Motor
motor1 = rsiStepMotor(STEP_PIN, DIRECTION_PIN, ENABLE_PIN)


rlsFirstCalibration = False
rlsSecondCalibration = False
rlsLockOut = False
def right_ls():
	global rlsFirstCalibration, rlsSecondCalibration, rlsLockOut
	if rlsLockOut:
		return
	
	if not rlsFirstCalibration:
		rlsFirstCalibration = True
		rlsLockOut = True
		return
	
	if not rlsSecondCalibration:
		rlsSecondCalibration = True
		rlsLockOut = True
		return


llsFirstCalibration = False
llsSecondCalibration = False
llsLockOut = False
def left_ls():
	global llsFirstCalibration, llsSecondCalibration, llsLockOut
	if llsLockOut:
		return
	
	if not llsFirstCalibration:
		llsFirstCalibration = True
		llsLockOut = True
		return
	
	if not llsSecondCalibration:
		llsSecondCalibration = True
		llsLockOut = True
		return


def calibrateTrack():
	global rlsFirstCalibration, rlsSecondCalibration, rlsLockOut, llsFirstCalibration, llsSecondCalibration, llsLockOut
	rlsFirstCalibration = False
	rlsSecondCalibration = False
	rlsLockOut = False
	llsFirstCalibration = False
	llsSecondCalibration = False
	llsLockOut = False
	tempHome = 0
	tempEnd = None

	while not (rlsFirstCalibration):
		motor1.moveMotor(1, True, 80, False)
	motor1.moveMotor(40, False, 40, False)
	rlsLockOut = False

	while not (rlsSecondCalibration):
		motor1.moveMotor(1, True, 5, False)
	motor1.moveMotor(20, True, 5, False)
	rlsLockOut = False
	motor1.overWriteCurrentPosition(tempHome)

	while not (llsFirstCalibration):
		motor1.moveMotor(1, False, 80, True)
	motor1.moveMotor(40, True, 40, True)
	llsLockOut = False

	while not (llsSecondCalibration):
		motor1.moveMotor(1, False, 5, True)
	motor1.moveMotor(20, True, 5, True)
	llsLockOut = False
	tempEnd = motor1.getCurrentPosition()

	motor1.calibrateTrack(tempHome, tempEnd)




		
    

#Setting Interrupts
llsHalt.when_pressed = lambda: motor1.haltMotor("Left Emergancy Limit Switch", True)
rlsHalt.when_pressed = lambda: motor1.haltMotor("Right Emergancy Limit Switch", True)
btnHalt.when_deactivated = lambda: motor1.haltMotor("E-Stop Button", True)
lls.when_pressed = left_ls
rls.when_pressed = right_ls

def main():
	try:
		calibrateTrack()
		sleep(3)
		tempTarget = motor1.getTrackSteps() / 2
		motor1.moveMotor(tempTarget, True, 70)
		if motor1.getCurrentPosition() == tempTarget:
			print("Step tracking test passed")
		else:
			print("Step tracking test failed")


	except Exception as e:
		print(f"Error: {e}")
	finally:
		motor1.haltMotor("Program Complete", True)


if __name__ == "__main__":
	main()
