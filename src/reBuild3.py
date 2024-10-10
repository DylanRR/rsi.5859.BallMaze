import staticVars as sVars
import staticEncoders as sEncoders
import staticLimitSwitches as sLimitSwitches
import staticMotorsv2 as sMotors
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

def calibrate_horizontal_track():
	print("Entered Horizontal Calibration Mode....")
	encodersLocked(True)
	print("Encoders Locked")
	leftSwitch = sLimitSwitches.HL_ls_cali
	rightSwitch = sLimitSwitches.HR_ls_cali
	hMotor = sMotors.horizontalMotors

	hMotor.pulseFactory(direction=False, condition=lambda: not leftSwitch.getFirstCalibration(), motor1=True, motor2=False, initialTargetSpeed=90)
	hMotor.pulseFactory(direction=True, iterations=200, motor1=True, motor2=False, initialTargetSpeed=50)
	leftSwitch.setLockedOut(False)
	hMotor.pulseFactory(direction=False, condition=lambda: not leftSwitch.getSecondCalibration(), motor1=True, motor2=False, initialTargetSpeed=5)
	hMotor.pulseFactory(direction=True, iterations=20, motor1=True, motor2=False, initialTargetSpeed=50)
	leftSwitch.setLockedOut(False)
	hMotor.overwritePosition(0)

	hMotor.pulseFactory(direction=True, condition=lambda: not rightSwitch.getFirstCalibration(), motor1=True, motor2=False, initialTargetSpeed=90)
	hMotor.pulseFactory(direction=False, iterations=200, motor1=True, motor2=False, initialTargetSpeed=50)
	rightSwitch.setLockedOut(False)
	hMotor.pulseFactory(direction=True, condition=lambda: not rightSwitch.getSecondCalibration(), motor1=True, motor2=False, initialTargetSpeed=5)
	hMotor.pulseFactory(direction=False, iterations=20, motor1=True, motor2=False, initialTargetSpeed=50)
	rightSwitch.setLockedOut(False)

	hMotor.setEndPosition(hMotor.getPosition())
	print("Calibration Complete....")
	encodersLocked(False)


def calibrate_vertical_track():
	print("Entered Vertical Calibration Mode....")
	encodersLocked(True)
	print("Encoders Locked")
	leftSwitch = sLimitSwitches.L_ls_cali
	rightSwitch = sLimitSwitches.R_ls_cali
	vMotors = sMotors.verticalMotors
	knownStepCount = 5000	#This is the known step count for the vertical track it needs to be manually calibrated

	def leftRightSwitchTrip():
		return True if leftSwitch.getFirstCalibration() or rightSwitch.getFirstCalibration() else False
	
	vMotors.pulseFactory(direction=True, condition= not leftRightSwitchTrip(), motor1=True, motor2=True, initialTargetSpeed=90)

	if not leftSwitch.getFirstCalibration():
		vMotors.pulseFactory(direction=True, condition=not leftSwitch.getFirstCalibration(), motor1=True, motor2=False, initialTargetSpeed=50)
	if not rightSwitch.getFirstCalibration():
		vMotors.pulseFactory(direction=True, condition=not rightSwitch.getFirstCalibration(), motor1=False, motor2=True, initialTargetSpeed=50)

	vMotors.pulseFactory(direction=False, iterations=300, motor1=True, motor2=True, initialTargetSpeed=60)

	leftSwitch.setLockedOut(False)
	rightSwitch.setLockedOut(False)

	def leftRightSwitchTrip2():
		return True if leftSwitch.getSecondCalibration() or rightSwitch.getSecondCalibration() else False
	
	vMotors.pulseFactory(direction=True, condition= not leftRightSwitchTrip2(), motor1=True, motor2=True, initialTargetSpeed=90)

	if not leftSwitch.getSecondCalibration():
		vMotors.pulseFactory(direction=True, condition=not leftSwitch.getSecondCalibration(), motor1=True, motor2=False, initialTargetSpeed=50)
	if not rightSwitch.getSecondCalibration():
		vMotors.pulseFactory(direction=True, condition=not rightSwitch.getSecondCalibration(), motor1=False, motor2=True, initialTargetSpeed=50)

	vMotors.pulseFactory(direction=False, iterations=300, motor1=True, motor2=True, initialTargetSpeed=60)

	vMotors.overwritePosition(knownStepCount) #If we want the top to be the end we would just set our current position to the known static end position
	vMotors.setEndPosition(knownStepCount)

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
	print("Moving Motor Up: ", m1DirToReSync)
	sMotors.motor1.moveUntilCondition(lambda: not mSync.isFineSynced(), m1DirToReSync, 85)
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
			print("De-Sync Detected....")
			encodersLocked(True)
			if thread_e1:
				thread_e1.join()
			if thread_e2:
				thread_e2.join()
			reSyncMotors()
			encodersLocked(False)
			print("Exiting Re-Sync....")
		
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
	calibrate_vertical_track()
	devMoveAllToCenter()
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