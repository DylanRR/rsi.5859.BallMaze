import staticVars as sVars
import staticEncoders as sEncoders
import staticLimitSwitches as sLimitSwitches
import staticMotors as sMotors
import sys
#from pot_calibration import MotorTracking as mTrack
import time
#import staticChips as sChips
from adafruit_ads1x15.ads1115 import ADS1115
import ads1115_wrapper
import board
import busio
import traceback
import threading


# Initialize the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c, address=0x48)
mSync = ads1115_wrapper.MotorSync(ads, 0, 1)


class mHaltException(Exception):
	def __init__(self, message):
		super().__init__(message)

def encodersLocked(locked):
	sEncoders.encoder1.ISR_LOCK(locked)
	sEncoders.encoder2.ISR_LOCK(locked)

def moveUntilCondition(motorObj: sMotors.rsiStepMotor, condition, steps, direction, speed, trackPos=True, rampOverride=False):
  while not condition():
    motorObj.moveMotor(steps, direction, speed, trackPos, rampOverride)

def calibrate_horizontal_track():
	print("Entered Calibration Mode....")
	encodersLocked(True)
	print("Encoders Locked")
	tempHome = 0
	tempEnd = None
	rightSwitch = sLimitSwitches.HL_ls_cali
	leftSwitch = sLimitSwitches.HR_ls_cali

	sMotors.motor2.enableMotor()
	leftSwitch.setLockedOut(True)
	moveUntilCondition(sMotors.motor2, lambda: rightSwitch.getFirstCalibration(), 1, True, 92, False)
	sMotors.motor2.moveMotor(200, False, 5, False)
	rightSwitch.setLockedOut(False)

	moveUntilCondition(sMotors.motor2, lambda: rightSwitch.getSecondCalibration(), 1, True, 5, False,)
	sMotors.motor2.moveMotor(20, True, 1, False)
	rightSwitch.setLockedOut(False)
	sMotors.motor2.overWriteCurrentPosition(tempHome)

	leftSwitch.setLockedOut(False)
	moveUntilCondition(sMotors.motor2, lambda: leftSwitch.getFirstCalibration(), 1, False, 92, True)
	sMotors.motor2.moveMotor(200, True, 5, True)
	leftSwitch.setLockedOut(False)

	moveUntilCondition(sMotors.motor2, lambda: leftSwitch.getSecondCalibration(), 1, False, 5, True)
	sMotors.motor2.moveMotor(20, True, 1, True)
	leftSwitch.setLockedOut(False)
	tempEnd = sMotors.motor2.getCurrentPosition()

	sMotors.motor2.calibrateTrack(tempHome, tempEnd)
	print("Calibration Complete....")
	encodersLocked(False)


def calibrate_vertical_track():
	print("Entered Calibration Mode....")
	encodersLocked(True)
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
			sMotors.motor1.moveMotor(1, True, 90, False)
		else:
			print ("Left Switch Hit")
			tempL = True
		if not rightSwitch.getFirstCalibration():
			sMotors.motor3.moveMotor(1, True, 90, False)	
		else:
			print ("Right Switch Hit")
			tempR = True
	print("First Calibration hit Complete....")

#Back off the motors slowly
	for _ in range(300):
		sMotors.motor1.moveMotor(1, False, 60, False)
		sMotors.motor3.moveMotor(1, False, 60, False)

	leftSwitch.setLockedOut(False)
	rightSwitch.setLockedOut(False)

	print("Back Off Complete....")

#Move the motors until the LS is hit for a second time
	tempL = False
	tempR = False
	while not tempL or not tempR:
		if not leftSwitch.getSecondCalibration():
			sMotors.motor1.moveMotor(1, True, 60, False)
		else:
			tempL = True
		if not rightSwitch.getSecondCalibration():
			sMotors.motor3.moveMotor(1, True, 60, False)
		else:
			tempR = True
	print("Second Calibration hit Complete....")

#Back off the motors slowly to home position
	for _ in range(300):
		sMotors.motor1.moveMotor(1, False, 60)
		sMotors.motor3.moveMotor(1, False, 60)
	
	print("Second Back Off Complete....")

	mSync.calibrate()
	'''
	sMotors.motor1.overWriteCurrentPosition(0)
	sMotors.motor3.overWriteCurrentPosition(0)
	while mSync.isCalibrationComplete():
		sMotors.motor1.moveMotor(1, False, 100, True)
		sMotors.motor3.moveMotor(1, False, 100, True)

	tempEnd1 = sMotors.motor1.getCurrentPosition()
	tempEnd2 = sMotors.motor3.getCurrentPosition()
	tempEnd = (tempEnd1 + tempEnd2) // 2

	sMotors.motor1.calibrateTrack(0, tempEnd)
	sMotors.motor3.calibrateTrack(0, tempEnd)
'''
	print("Calibration Complete....")
	encodersLocked(False)


def checkException():
	if sMotors.motors_halted:
		raise mHaltException(sMotors.halt_reason)
	
def garbageCollection():
	sMotors.cleanup()
	sEncoders.cleanup()
	sLimitSwitches.cleanup()


def reSyncMotors():
	print("Re-Syncing Motors....")
	m1DirToReSync = mSync.getReSyncDirection()
	sMotors.motor1.moveUntilCondition(lambda: not mSync.isDeSynced(), m1DirToReSync, 1)
	tempPos = sMotors.motor1.getCurrentPosition()
	sMotors.motor1.moveUntilCondition(lambda: mSync.isDeSynced(), m1DirToReSync, 1)
	tempPos2 = sMotors.motor1.getCurrentPosition()
	stepsToMiddle = abs(tempPos - tempPos2) // 2
	sMotors.motor1.moveMotor(stepsToMiddle, not m1DirToReSync, 1)
	sMotors.motor1.overWriteCurrentPosition(sMotors.motor2.getCurrentPosition())
	if mSync.isDeSynced():
		raise mHaltException("Re-Sync Failed")
	else:
		print("Re-Sync Completed successfully ....")

def run_in_thread():
	multiplier = 1
	while sEncoders.encoder2.isEncoderRunning():
		sMotors.motor2.moveMotor(1, sEncoders.encoder2.direction, abs(sEncoders.encoder2.getSpeed() + multiplier))
def run_in_second_thread():
	multiplier = 1.5
	while sEncoders.encoder1.isEncoderRunning():
		sMotors.motor1.moveMotor(1, sEncoders.encoder1.direction, abs(sEncoders.encoder1.getSpeed() + multiplier))
		sMotors.motor3.moveMotor(1, sEncoders.encoder1.direction, abs(sEncoders.encoder1.getSpeed() + multiplier))

# Main function to manage threads
def IR_RUN_STATE():
	thread_e1 = None
	thread_e2 = None

	while True:
		e1_state = sEncoders.encoder1.isEncoderRunning()
		e2_state = sEncoders.encoder2.isEncoderRunning()

		if not e1_state and not e2_state:
			break

		if e1_state and (thread_e1 is None or not thread_e1.is_alive()):
			thread_e1 = threading.Thread(target=run_in_second_thread)
			thread_e1.start()

		if e2_state and (thread_e2 is None or not thread_e2.is_alive()):
			thread_e2 = threading.Thread(target=run_in_thread)
			thread_e2.start()

		if e1_state and (thread_e1 is None or not thread_e1.is_alive()):
			tempDir = sEncoders.encoder1.direction
			tempSpeed = sEncoders.encoder1.getSpeed()
			sMotors.motor1.setDirection(tempDir)
			sMotors.motor1.setPower(tempSpeed)
			sMotors.motor3.setDirection(tempDir)
			sMotors.motor3.setPower(tempSpeed)

		if e2_state and (thread_e2 is None or not thread_e2.is_alive()):
			sMotors.motor2.setDirection(sEncoders.encoder2.direction)
			sMotors.motor2.setPower(sEncoders.encoder2.getSpeed())

		if mSync.isDeSynced():
			encodersLocked(True)
			if thread_e1:
				thread_e1.join()
			if thread_e2:
				thread_e2.join()
			reSyncMotors()
		
		time.sleep(0.1)  # Prevents the CPU from being overloaded

	# Ensure threads are properly joined
	if thread_e1:
		thread_e1.join()
	if thread_e2:
		thread_e2.join()


def devMoveAllToCenter():
	steps = sMotors.motor2.getTrackSteps() // 2
	for _ in range(steps):
		sMotors.motor2.moveMotor(1, True, 92)
		sMotors.motor1.moveMotor(1, False, 92)
		sMotors.motor3.moveMotor(1, False, 92)

def devScript():
	calibrate_horizontal_track()
	#calibrate_vertical_track()
	#devMoveAllToCenter()
	input("Press Enter to continue...")  # Pause and wait for user input
	while True:
		IR_RUN_STATE()

def main():
	testCal = False
	try:
		while True:
			checkException()
			#if testCal:
			#	raise mHaltException("Test Calibration Complete")
			devScript()
			pass
			testCal = True
	
	except KeyboardInterrupt:
		print("KeyboardInterrupt Triggered Killing the program...")
		sMotors.disableAllMotors()
	except mHaltException as lsObj:
		print(f"Stoppage Triggered By: {lsObj}")
	except Exception as e:
		sMotors.disableAllMotors()
		print(e)
		traceback.print_exc()
	finally:
		sMotors.disableAllMotors()
		garbageCollection()
		sys.exit(0)

if __name__ == "__main__":
	main()