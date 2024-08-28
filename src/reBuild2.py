import staticVars as sVars
from staticVars import motor1, motor2, motor3, encoder1, encoder2, motors, encoders, limitSwitches, haltingLimitSwitches
from rsiStepMotor import rsiStepMotor, mHaltException
from limitSwitch import mHaltException as lsHaltException
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
	moveUntilCondition(motor2, lambda: rightSwitch.getFirstCalibration(), 1, True, 95, False)
	motor2.moveMotor(200, False, 5, False)
	rightSwitch.setLockedOut(False)

	moveUntilCondition(motor2, lambda: rightSwitch.getSecondCalibration(), 1, True, 5, False,)
	motor2.moveMotor(20, True, 1, False)
	rightSwitch.setLockedOut(False)
	motor2.overWriteCurrentPosition(tempHome)

	leftSwitch.setLockedOut(False)
	moveUntilCondition(motor2, lambda: leftSwitch.getFirstCalibration(), 1, False, 95, True)
	motor2.moveMotor(200, True, 5, True)
	leftSwitch.setLockedOut(False)

	moveUntilCondition(motor2, lambda: leftSwitch.getSecondCalibration(), 1, False, 5, True)
	motor2.moveMotor(20, True, 1, True)
	leftSwitch.setLockedOut(False)
	tempEnd = motor2.getCurrentPosition()

	motor2.calibrateTrack(tempHome, tempEnd)
	moveToCenter(motor2)
	print("Calibration Complete....")
	encoderLocked(False)


def IR_RUN_STATE():
	if encoder2.isEncoderRunning():
		while encoder2.isEncoderRunning():
			motor2.moveMotor(motor2.getStepIncrement(), encoder2.direction, encoder2.getSpeed())
			
def disableAllMotors():
	for motor in motors:
		motor.disableMotor()

def main():
	try:
		calibrate_horizontal_track()
	except (lsHaltException, mHaltException) as raisedMsg:
		print(raisedMsg)
		disableAllMotors()
	except KeyboardInterrupt:
		print("Exiting Program")
		disableAllMotors()
	except Exception as e:
		print(e)
		disableAllMotors()
	finally:
		sVars.cleanup()
		sys.exit(0)

if __name__ == "__main__":
	main()