import staticVars as sVars
import staticEncoders as sEncoders
import staticLimitSwitches as sLimitSwitches
import staticMotors as sMotors
import sys
import time

class mHaltException(Exception):
	def __init__(self, message):
		super().__init__(message)

def encoderLocked(locked):
	sEncoders.encoder1.ISR_LOCK(locked)
	sEncoders.encoder2.ISR_LOCK(locked)

def moveUntilCondition(motorObj: sMotors.rsiStepMotor, condition, steps, direction, speed, trackPos=True, rampOverride=False):
  while not condition():
    motorObj.moveMotor(steps, direction, speed, trackPos, rampOverride)

def moveToCenter(motorObj: sMotors.rsiStepMotor, speed=98):
	print("Moving to Center")
	motorObj.moveMotor(motorObj.getTrackSteps() // 2, True, speed)

def calibrate_horizontal_track():
	print("Entered Calibration Mode....")
	encoderLocked(True)
	print("Encoders Locked")
	tempHome = 0
	tempEnd = None
	rightSwitch = sLimitSwitches.HL_ls_cali
	leftSwitch = sLimitSwitches.HR_ls_cali

	sMotors.motor2.enableMotor()
	leftSwitch.setLockedOut(True)
	moveUntilCondition(sMotors.motor2, lambda: rightSwitch.getFirstCalibration(), 1, True, 98, False)
	sMotors.motor2.moveMotor(200, False, 5, False)
	rightSwitch.setLockedOut(False)

	moveUntilCondition(sMotors.motor2, lambda: rightSwitch.getSecondCalibration(), 1, True, 5, False,)
	sMotors.motor2.moveMotor(20, True, 1, False)
	rightSwitch.setLockedOut(False)
	sMotors.motor2.overWriteCurrentPosition(tempHome)

	leftSwitch.setLockedOut(False)
	moveUntilCondition(sMotors.motor2, lambda: leftSwitch.getFirstCalibration(), 1, False, 98, True)
	sMotors.motor2.moveMotor(200, True, 5, True)
	leftSwitch.setLockedOut(False)

	moveUntilCondition(sMotors.motor2, lambda: leftSwitch.getSecondCalibration(), 1, False, 5, True)
	sMotors.motor2.moveMotor(20, True, 1, True)
	leftSwitch.setLockedOut(False)
	tempEnd = sMotors.motor2.getCurrentPosition()

	sMotors.motor2.calibrateTrack(tempHome, tempEnd)
	moveToCenter(sMotors.motor2)
	print("Calibration Complete....")
	encoderLocked(False)


def IR_RUN_STATE():
	if sEncoders.encoder2.isEncoderRunning():
		while sEncoders.encoder2.isEncoderRunning():
			sMotors.motor2.moveMotor(sMotors.motor2.getStepIncrement(), sEncoders.encoder2.direction, sEncoders.encoder2.getSpeed())
			
def checkException():
	if sMotors.motors_halted:
		raise mHaltException(sMotors.halt_reason)
	
def garbageCollection():
	sMotors.cleanup()
	sEncoders.cleanup()
	sLimitSwitches.cleanup()

def main():
	testCal = False
	try:
		while True:
			checkException()
			if testCal:
				raise mHaltException("Test Calibration Complete")
			calibrate_horizontal_track()
			testCal = True
			#sMotors.motor2.enableMotor()
			#sMotors.motor2.moveMotor(1000, False, 95)
	
	except KeyboardInterrupt:
		print("KeyboardInterrupt Triggered Killing the program...")
		sMotors.disableAllMotors()
	except mHaltException as lsObj:
		print(f"Stoppage Triggered By: {lsObj}")
	except Exception as e:
		print(e)
		sMotors.disableAllMotors()
	finally:
		sMotors.disableAllMotors()
		garbageCollection()
		sys.exit(0)

if __name__ == "__main__":
	main()