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


# Initialize the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c, address=0x48)
mSync = ads1115_wrapper.MotorSync(ads, 0, 1)


class mHaltException(Exception):
	def __init__(self, message):
		super().__init__(message)

def encoderLocked(locked):
	sEncoders.encoder1.ISR_LOCK(locked)
	sEncoders.encoder2.ISR_LOCK(locked)

def moveUntilCondition(motorObj: sMotors.rsiStepMotor, condition, steps, direction, speed, trackPos=True, rampOverride=False):
  while not condition():
    motorObj.moveMotor(steps, direction, speed, trackPos, rampOverride)


def moveToCenter(motorObj: sMotors.rsiStepMotor, speed=97):
	print("Moving to Center")
	motorObj.moveMotor(motorObj.getTrackSteps() // 2, True, speed)

def moveToHome(motorObj: sMotors.rsiStepMotor, speed=97):
	print("Moving to Home")
	motorObj.moveMotor(motorObj.getTrackSteps()-200, True, speed)

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
	moveUntilCondition(sMotors.motor2, lambda: rightSwitch.getFirstCalibration(), 1, True, 90, False)
	sMotors.motor2.moveMotor(200, False, 5, False)
	rightSwitch.setLockedOut(False)

	moveUntilCondition(sMotors.motor2, lambda: rightSwitch.getSecondCalibration(), 1, True, 5, False,)
	sMotors.motor2.moveMotor(20, True, 1, False)
	rightSwitch.setLockedOut(False)
	sMotors.motor2.overWriteCurrentPosition(tempHome)

	leftSwitch.setLockedOut(False)
	moveUntilCondition(sMotors.motor2, lambda: leftSwitch.getFirstCalibration(), 1, False, 90, True)
	sMotors.motor2.moveMotor(200, True, 5, True)
	leftSwitch.setLockedOut(False)

	moveUntilCondition(sMotors.motor2, lambda: leftSwitch.getSecondCalibration(), 1, False, 5, True)
	sMotors.motor2.moveMotor(20, True, 1, True)
	leftSwitch.setLockedOut(False)
	tempEnd = sMotors.motor2.getCurrentPosition()

	sMotors.motor2.calibrateTrack(tempHome, tempEnd)
	#moveToCenter(sMotors.motor2)
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
			sMotors.motor1.moveMotor(1, True, 90)
		else:
			print ("Left Switch Hit")
			tempL = True
		if not rightSwitch.getFirstCalibration():
			sMotors.motor3.moveMotor(1, True, 90)	
		else:
			print ("Right Switch Hit")
			tempR = True
	print("First Calibration hit Complete....")

#Back off the motors slowly
	for _ in range(300):
		sMotors.motor1.moveMotor(1, False, 60)
		sMotors.motor3.moveMotor(1, False, 60)

	leftSwitch.setLockedOut(False)
	rightSwitch.setLockedOut(False)

	print("Back Off Complete....")

#Move the motors until the LS is hit for a second time
	tempL = False
	tempR = False
	while not tempL or not tempR:
		if not leftSwitch.getSecondCalibration():
			sMotors.motor1.moveMotor(1, True, 60)
		else:
			tempL = True
		if not rightSwitch.getSecondCalibration():
			sMotors.motor3.moveMotor(1, True, 60)
		else:
			tempR = True
	print("Second Calibration hit Complete....")

#Back off the motors slowly to home position
	for _ in range(300):
		sMotors.motor1.moveMotor(1, False, 60)
		sMotors.motor3.moveMotor(1, False, 60)
	
	print("Second Back Off Complete....")

	mSync.calibrate()
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

def checkSync(current_direction):
	behind_motor, moveInstruction = mSync.getSyncInstructions()
	#Guarding statement in case things have changed since calling isDeSynced
	if behind_motor == 0:
		return

	if behind_motor == 1:			#Motor 1 needs to catchup 
		steps = sMotors.motor1.getTrackSteps() * (moveInstruction / 100)
		if current_direction:
			sMotors.motor1.moveMotor(steps, True, 60)
		else:
			sMotors.motor1.moveMotor(steps, False, 60)
	else:											#Motor 3 needs to catchup
		steps = sMotors.motor3.getTrackSteps() * (moveInstruction / 100)
		if current_direction:
			sMotors.motor3.moveMotor(steps, True, 60)
		else:
			sMotors.motor3.moveMotor(steps, False, 60)

	#Recursively call checkSync until we are synced
	if mSync.isDeSynced():
		checkSync()



def devTestMotorSync(steps, direction, speed):
	for i in range(steps):
		sMotors.motor1.moveMotor(1, direction, speed)
		sMotors.motor3.moveMotor(1, direction, speed)
		if mSync.isDeSynced():
			checkSync(direction)



def devIR_RUN_STATE():
	e1_state = sEncoders.encoder1.isEncoderRunning()
	e2_state = sEncoders.encoder2.isEncoderRunning()
	#Encoder 1 = Vertical movement       Encoder 2 = Horizontal movement
	if e1_state & e2_state:
		while sEncoders.encoder1.isEncoderRunning() & sEncoders.encoder2.isEncoderRunning():
			sMotors.motor2.moveMotor(1, sEncoders.encoder2.direction, sEncoders.encoder2.getSpeed())
			e1_dir = sEncoders.encoder1.direction
			e1_speed = sEncoders.encoder1.getSpeed()
			sMotors.motor1.moveMotor(1, e1_dir, e1_speed)
			sMotors.motor3.moveMotor(1, e1_dir, e1_speed)
			if mSync.isDeSynced():
				checkSync()
	elif e1_state:
		pass
	elif e2_state:
		pass
	



def devVertMoveNoCal(steps, direction, speed):
	m2Dir = not direction
	for _ in range(steps):
		sMotors.motor1.moveMotor(1, direction, speed, True)
		sMotors.motor2.moveMotor(1, m2Dir, speed, True)
		sMotors.motor3.moveMotor(1, direction, speed, True)
			


def devScript():
	calibrate_horizontal_track()
	#devVerticalMotorMove(8000, True, 60)
	calibrate_vertical_track()
	#devVerticalMotorMove(12000, False, 98)
	input("Press Enter to continue...")  # Pause and wait for user input
	testStep = sMotors.motor2.getTrackSteps()-200
	devTestMotorSync(testStep, False, 99)
	#devVertMoveNoCal(testStep, False, 99)
	#moveToHome(sMotors.motor2)

def devScript2():
	while True:
		input("Press Enter to Enable Motor 2...")  # Pause and wait for user input
		sMotors.motor2.enableMotor()
		input("Press Enter to Disable Motor 2...")  # Pause and wait for user input
		sMotors.motor2.disableMotor()

def main():

	testCal = False
	try:
		while True:
			checkException()
			if testCal:
				raise mHaltException("Test Calibration Complete")
			#sMotors.motor2.enableMotor()
			devScript()
			#devScript2()
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