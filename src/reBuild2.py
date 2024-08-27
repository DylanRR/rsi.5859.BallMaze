import staticVars as sVars
from staticVars import motor1, motor2, motor3, encoder1, encoder2
from rsiStepMotor import rsiStepMotor
import sys


def encoderLocked(locked):
	sVars.encoder1.ISR_LOCK(locked)
	sVars.encoder2.ISR_LOCK(locked)

def moveUntilCondition(motorObj: rsiStepMotor, condition, steps, direction, speed, trackPos=True, rampOverride=False):
  while not condition():
    motorObj.moveMotor(steps, direction, speed, trackPos, rampOverride)

def moveToCenter(motorObj: rsiStepMotor, speed=95):
	print("Moving to Center")
	motorObj.moveMotor(motorObj.getTrackSteps() // 2, True, speed)

def calibrate_horizontal_track():
	print("Entered Calibration Mode....")
	encoderLocked(True)
	print("Encoders Locked")
	tempHome = 0
	tempEnd = None
	leftSwitch = sVars.HL_ls_cali
	rightSwitch = sVars.HR_ls_cali

	motor2.enableMotor()
	leftSwitch.setLockedOut(True)
	moveUntilCondition(lambda: rightSwitch.getFirstCalibration(), 1, True, 95, False)
	motor2.moveMotor(200, False, 5, False)
	rightSwitch.setLockedOut(False)

	moveUntilCondition(lambda: rightSwitch.getSecondCalibration(), 1, True, 5, False,)
	motor2.moveMotor(20, True, 1, False)
	rightSwitch.setLockedOut(False)
	motor2.overWriteCurrentPosition(tempHome)

	leftSwitch.setLockedOut(False)
	moveUntilCondition(lambda: leftSwitch.getFirstCalibration(), 1, False, 95, True)
	motor2.moveMotor(200, True, 5, True)
	leftSwitch.setLockedOut(False)

	moveUntilCondition(lambda: leftSwitch.getSecondCalibration(), 1, False, 5, True)
	motor2.moveMotor(20, True, 1, True)
	leftSwitch.setLockedOut(False)
	tempEnd = motor2.getCurrentPosition()

	motor2.calibrateTrack(tempHome, tempEnd)
	moveToCenter(motor2)
	print("Calibration Complete....")
	encoderLocked(False)


def IR_RUN_STATE():
	if encoder1.isEncoderRunning():
		while encoder1.isEncoderRunning():
			motor1.moveMotor(motor1.getStepIncrement(), encoder1.direction, encoder1.getSpeed())
			

def main():
	try:
		calibrate_horizontal_track()
		while True:
			#break
			#IR_RUN_STATE()
			pass
	except Exception as e:
		print(f"Error: {e}")
		motor1.haltMotor("Internal Error", False)
		motor2.haltMotor("Internal Error", False)
		motor3.haltMotor("Internal Error", True)
	finally:
		motor1.haltMotor("Program Complete", False)
		motor2.haltMotor("Program Complete", False)
		motor3.haltMotor("Program Complete", True)
		sys.exit(1)


if __name__ == "__main__":
	main()