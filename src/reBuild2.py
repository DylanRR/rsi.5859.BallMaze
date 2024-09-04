import staticVars as sVars
import staticEncoders as sEncoders
import staticLimitSwitches as sLimitSwitches
import staticMotors as sMotors
import sys
from pot_calibration import MotorTracking as mTrack


pCal = mTrack(sVars.m1McpChannel, sVars.m2McpChannel)

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


def calibrate_vertical_track():
	print("Entered Calibration Mode....")
	encoderLocked(True)
	print("Encoders Locked")
	tempHome = 0
	tempEnd = None
	leftSwitch = sLimitSwitches.L_ls_cali
	rightSwitch = sLimitSwitches.R_ls_cali
	tempL = False
	tempR = False

#Move the motors until first LS is hit
	while not tempL or not tempR:
		if not leftSwitch.getFirstCalibration():
			sMotors.motor1.moveMotor(1, True, 85)
		else:
			tempL = True
		if not rightSwitch.getFirstCalibration():
			sMotors.motor3.moveMotor(1, True, 85)	
		else:
			tempR = True

#Back off the motors slowly
	for _ in range(20):
		sMotors.motor1.moveMotor(1, False, 5)
		sMotors.motor3.moveMotor(1, False, 5)

#Move the motors until the LS is hit for a second time
	tempL = False
	tempR = False
	while not tempL or not tempR:
		if not leftSwitch.getSecondCalibration():
			sMotors.motor1.moveMotor(1, True, 5)
		else:
			tempL = True
		if not rightSwitch.getSecondCalibration():
			sMotors.motor3.moveMotor(1, True, 5)
		else:
			tempR = True

#Back off the motors slowly to home position
	for _ in range(20):
		sMotors.motor1.moveMotor(1, False, 1)
		sMotors.motor3.moveMotor(1, False, 1)

	pCal.calibrate()
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


#	Every 5 steps we check for a delta offset and adjust the motors accordingly.
#	If the motors do require adjustment we will continue to adjust them 
# with every step until the motors are back in sync.
def devVerticalMotorMove(steps, direction, speed):
	requireCalibration = False
	for i in range(steps):
		if ((i + 1) % 5 == 0) or requireCalibration:
			temp = pCal.checkForDeltaOffset(direction)
			if temp == 1:
				requireCalibration = True
				sMotors.motor1.moveMotor(1, direction, speed, True)
			elif temp == 2:
				requireCalibration = True
				sMotors.motor3.moveMotor(1, direction, speed, True)
		else:
			preformP_cal = False
			sMotors.motor1.moveMotor(1, direction, speed, True)
			sMotors.motor3.moveMotor(1, direction, speed, True)
			


def devScript():
	#calibrate_horizontal_track()
	devVerticalMotorMove(8000, True, 60)


def main():
	testCal = False
	try:
		while True:
			checkException()
			if testCal:
				raise mHaltException("Test Calibration Complete")
			devScript()
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