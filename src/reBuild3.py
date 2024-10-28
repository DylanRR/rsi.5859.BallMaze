import staticVars as sVars
import staticEncoders as sEncoders
import staticLimitSwitches as sLimitSwitches
import staticMotorsv2 as sMotors
import staticMCP as sMCP
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
import collections


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

	hMotor.pulseFactory(direction=True, condition=lambda: not leftSwitch.getFirstCalibration(), motor1=True, motor2=False, initialTargetSpeed=96)
	hMotor.pulseFactory(direction=False, iterations=200, motor1=True, motor2=False, initialTargetSpeed=10) #TODO: Magic Number
	leftSwitch.setLockedOut(False)
	hMotor.pulseFactory(direction=True, condition=lambda: not leftSwitch.getSecondCalibration(), motor1=True, motor2=False, initialTargetSpeed=80)
	hMotor.pulseFactory(direction=False, iterations=100, motor1=True, motor2=False, initialTargetSpeed=10) #TODO: Magic Number
	leftSwitch.setLockedOut(False)
	hMotor.overwritePosition(0)

	hMotor.pulseFactory(direction=False, condition=lambda: not rightSwitch.getFirstCalibration(), motor1=True, motor2=False, initialTargetSpeed=96)
	hMotor.pulseFactory(direction=True, iterations=200, motor1=True, motor2=False, initialTargetSpeed=10) #TODO: Magic Number
	rightSwitch.setLockedOut(False)
	hMotor.pulseFactory(direction=False, condition=lambda: not rightSwitch.getSecondCalibration(), motor1=True, motor2=False, initialTargetSpeed=80)
	hMotor.pulseFactory(direction=True, iterations=100, motor1=True, motor2=False, initialTargetSpeed=10) #TODO: Magic Number
	rightSwitch.setLockedOut(False)

	hMotor.setEndPosition(abs(hMotor.getPosition()))
	hMotor.overwritePosition(0)
	print("Calibration Complete....")
	encodersLocked(False)


def calibrate_vertical_track():
	print("Entered Vertical Calibration Mode....")
	encodersLocked(True)
	print("Encoders Locked")
	leftSwitch = sLimitSwitches.L_ls_cali
	rightSwitch = sLimitSwitches.R_ls_cali
	vMotors = sMotors.verticalMotors
	knownStepCount = 18496	#TODO: Magic Number - The Full calibrated step count for the vertical motor is 18760 we are backing it off 160 steps

	def leftRightSwitchTrip():
		return True if leftSwitch.getFirstCalibration() or rightSwitch.getFirstCalibration() else False
	
	vMotors.pulseFactory(direction=True, condition= lambda:not leftRightSwitchTrip(), motor1=True, motor2=True, initialTargetSpeed=90) #TODO: Magic Number

	if not leftSwitch.getFirstCalibration():
		vMotors.pulseFactory(direction=True, condition=lambda:not leftSwitch.getFirstCalibration(), motor1=True, motor2=False, initialTargetSpeed=50) #TODO: Magic Number
	if not rightSwitch.getFirstCalibration():
		vMotors.pulseFactory(direction=True, condition=lambda:not rightSwitch.getFirstCalibration(), motor1=False, motor2=True, initialTargetSpeed=50) #TODO: Magic Number

	vMotors.pulseFactory(direction=False, iterations=300, motor1=True, motor2=True, initialTargetSpeed=60)  #TODO: Magic Number

	leftSwitch.setLockedOut(False)
	rightSwitch.setLockedOut(False)

	def leftRightSwitchTrip2():
		return True if leftSwitch.getSecondCalibration() or rightSwitch.getSecondCalibration() else False
	
	vMotors.pulseFactory(direction=True, condition=lambda: not leftRightSwitchTrip2(), motor1=True, motor2=True, initialTargetSpeed=90) #TODO: Magic Number

	if not leftSwitch.getSecondCalibration():
		vMotors.pulseFactory(direction=True, condition=lambda:not leftSwitch.getSecondCalibration(), motor1=True, motor2=False, initialTargetSpeed=50) #TODO: Magic Number
	if not rightSwitch.getSecondCalibration():
		vMotors.pulseFactory(direction=True, condition=lambda:not rightSwitch.getSecondCalibration(), motor1=False, motor2=True, initialTargetSpeed=50) #TODO: Magic Number

	#chaning from  300 iterations to 3000 iterations to move down the gantry for brian
	vMotors.pulseFactory(direction=False, iterations=300, motor1=True, motor2=True, initialTargetSpeed=80) #TODO: Magic Number

	vMotors.setEndPosition(knownStepCount)
	vMotors.overwritePosition(knownStepCount)
	mSync.calibrate()

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
	vMotors = sMotors.verticalMotors
	print("Moving Motor Up: ", m1DirToReSync)
	tempPos = vMotors.getPosition()
	vMotors.pulseFactory(direction=m1DirToReSync, condition=lambda: not mSync.isFineSynced(), motor1=True, motor2=False, initialTargetSpeed=85) #TODO: Magic Number
	tempPos = abs(tempPos - vMotors.getPosition()) // 2
	vMotors.overwritePosition(tempPos)
	if mSync.isDeSynced():
		raise mHaltException("Re-Sync Failed")
	else:
		print("Re-Sync Completed successfully ....")


def sendToHome():
	print("Sending Motors to Home....")
	sMCP.homing_LED.turnOn()
	currentHCord = sMotors.horizontalMotors.getPosition()
	currentVCord = sMotors.verticalMotors.getPosition()
	hMotorHomeCords = 22745		#TODO: Magic Number
	vMotorHomeCords = 0				#TODO: Magic Number

	hMotorDirToHome = False if currentHCord > hMotorHomeCords else True
	vMotorDirToHome = False if currentVCord > vMotorHomeCords else True
	vMotorStepsToHome = abs(currentVCord - vMotorHomeCords)
	hMotorStepsToHome = abs(currentHCord - hMotorHomeCords)

	def hHomeMove():
		sMotors.horizontalMotors.pulseFactory(direction=hMotorDirToHome, iterations=hMotorStepsToHome, motor1=True, motor2=False, initialTargetSpeed=95) #TODO: Magic Number
	def vHomeMove():
		sMotors.verticalMotors.pulseFactory(direction=vMotorDirToHome, iterations=vMotorStepsToHome, motor1=True, motor2=True, initialTargetSpeed=95) #TODO: Magic Number

	hHomeMoveThread = threading.Thread(target=hHomeMove)
	vHomeMoveThread = threading.Thread(target=vHomeMove)
	hHomeMoveThread.start()
	vHomeMoveThread.start()
	hHomeMoveThread.join()
	vHomeMoveThread.join()
	sMCP.homing_LED.turnOff()

def run_in_thread():
	print ("Running Horizontal Motor....")
	sMCP.Encoder2_LED.turnOn()
	hMotor = sMotors.horizontalMotors
	encoder = sEncoders.encoder2
	tempDir = encoder.direction
	initSpeed = encoder.getSpeed()
	tempEndPos = hMotor.getEndPosition()

	def continuePulsing():
		if not encoder.isEncoderRunning():
			print("Horizontal Motor Encoder is not running")
			return False
		if encoder.hasDirChanged(tempDir):
			print("Horizontal Motor Encoder Direction Changed")
			return False
		if tempDir:
			if hMotor.getPosition() >= tempEndPos:
				print("Horizontal Motor Position End Reached")
				return False
		elif hMotor.getPosition() <= 0:
			print("Horizontal Motor Position End Reached")
			return False
		return True
	
	if continuePulsing():
		hMotor.pulseFactory(direction=tempDir, condition= lambda: continuePulsing(), motor1=True, motor2=False, initialTargetSpeed=80)  #Changing initialTargetSpeed=initSpeed to initialTargetSpeed=80
	sMCP.Encoder2_LED.turnOff()

def devRunInFirstThread():
	tempDir = sEncoders.encoder2.direction
	print (f"Running H Thread,  Dir:  {tempDir}")
	while not sEncoders.encoder2.hasDirChanged(tempDir):
		# Motor Running Here
		time.sleep(0.1)
	time.sleep (0.1)

def devRunInSecondThread():
	print ("Running Vertical Thread")
	tempDir = sEncoders.encoder1.direction
	print (f"V Thread Dir:  {tempDir}")
	while not sEncoders.encoder1.hasDirChanged(tempDir):
		# Motor Running Here
		time.sleep(0.1)
	print (f"Breaking V Thread,  new Dir:  {sEncoders.encoder1.direction}")
	time.sleep (0.1)

def run_in_second_thread():
	print ("Running Virtual Motor....")
	sMCP.Encoder1_LED.turnOn()
	vMotor = sMotors.verticalMotors
	encoder = sEncoders.encoder1
	tempDir = encoder.getDirection()
	initSpeed = encoder.getSpeed()
	tempEndPos = vMotor.getEndPosition()
	def continuePulsing():
		if not encoder.isEncoderRunning():
			print("Vertical Motor Encoder is not running")
			return False
		if encoder.hasDirChanged(tempDir):
			print("Vertical Motor Encoder Direction Changed")
			return False
		if tempDir:
			if vMotor.getPosition() >= tempEndPos:
				print("Vertical Motor Position End Reached")
				return False
		elif vMotor.getPosition() <= 0:
				print("Vertical Motor Position End Reached")
				return False
		return True
	if continuePulsing():
		vMotor.pulseFactory(direction=tempDir, condition= lambda: continuePulsing(), motor1=True, motor2=True, initialTargetSpeed=80)  #Changing initialTargetSpeed=initSpeed to initialTargetSpeed=80
	sMCP.Encoder1_LED.turnOff()


# Main function to manage threads
def IR_RUN_STATE():
	thread_e1 = None
	thread_e2 = None
	hMotor = sMotors.horizontalMotors
	vMotor = sMotors.verticalMotors
	vEncode = sEncoders.encoder1
	hEncode = sEncoders.encoder2
	lastVSpeedUpdate = time.time()
	lastHSPeedUpdate = time.time()
	speedUpdateInterval = 1
	hSpeedBuffer = collections.deque(maxlen=5)
	vSpeedBuffer = collections.deque(maxlen=5)

	while True:
		e1_state = sEncoders.encoder1.isEncoderRunning()
		e2_state = sEncoders.encoder2.isEncoderRunning()

		if not e1_state and not e2_state:
			break

		if e1_state and (thread_e1 is None or not thread_e1.is_alive()):
			thread_e1 = threading.Thread(target=devRunInSecondThread) #Changing target=run_in_second_thread
			thread_e1.start()

		if e2_state and (thread_e2 is None or not thread_e2.is_alive()):
			thread_e2 = threading.Thread(target=devRunInFirstThread)	#Changing target=run_in_thread
			thread_e2.start()


		'''
		if e1_state and thread_e1.is_alive():
			vSpeedBuffer.append(vEncode.getSpeed())
			if time.time() - lastVSpeedUpdate > speedUpdateInterval:
				vMotor.setTargetSpeed(sum(vSpeedBuffer) // len(vSpeedBuffer))
				lastVSpeedUpdate = time.time()

		if e2_state and thread_e2.is_alive():
			hSpeedBuffer.append(hEncode.getSpeed())
			if time.time() - lastHSPeedUpdate > speedUpdateInterval:
				hMotor.setTargetSpeed(sum(hSpeedBuffer) // len(hSpeedBuffer))
				lastHSPeedUpdate = time.time()
		'''

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

		'''
		if not sMCP.breakBeam_SENS.getVal():
			print("Break Beam Triggered....")
			sMCP.Ir_LED.turnOff()
			sMCP.breakBeam_LED.turnOn()
			encodersLocked(True)
			if thread_e1:
				thread_e1.join()
			if thread_e2:
				thread_e2.join()
			sendToHome()
			encodersLocked(False)
			sMCP.breakBeam_LED.turnOff()
			sMCP.Ir_LED.turnOn()
		'''
		time.sleep(0.1)  # Prevents the CPU from being overloaded

	# Ensure threads are properly joined
	if thread_e1:
		thread_e1.join()
	if thread_e2:
		thread_e2.join()


#Utility function to calculate the vertical steps
def devCalculateVertSteps():
	print("Calculating Vertical Steps....")
	vMotors = sMotors.verticalMotors
	vMotors.overwritePosition(0)
	print("Current Position Overrided to: ", vMotors.getPosition())
	print("Moveing motor down till Estop is triggered....")
	def devIsHaulted():
		return sMotors.motors_halted
	vMotors.pulseFactory(direction=False, condition=lambda: not devIsHaulted(), motor1=True, motor2=True, initialTargetSpeed=20) #TODO: Magic Number
	print("Estop Trigger Detected....")
	print("Current Vertical Motor Position: ", abs(vMotors.getPosition()))
	print("Raising Exeption")
	checkException()




def devScript():
	print("Entered Development Script....")
	def moveThread1():
		sMotors.verticalMotors.pulseFactory(direction=False, iterations=4000, motor1=True, motor2=True, initialTargetSpeed=5) #TODO: Magic Number
	
	def moveThread2():
		sMotors.horizontalMotors.pulseFactory(direction=False, iterations=4000, motor1=True, motor2=False, initialTargetSpeed=5)

	plock = threading.Lock()
	def printEncoder1():
		while True:
			with plock:
				print (f"Encoder 1 Dir: {sEncoders.encoder1.direction}")
			time.sleep(0.1)

	def printEncoder2():
		while True:
			with plock:
				print (f"Encoder 2 Dir: {sEncoders.encoder2.direction}")
			time.sleep(0.1)


	thread1 = threading.Thread(target=moveThread1)
	thread2 = threading.Thread(target=moveThread2)
	eThread1 = threading.Thread(target=printEncoder1)
	eThread2 = threading.Thread(target=printEncoder2)
	thread1.start()
	thread2.start()
	eThread1.start()
	eThread2.start()

	while True:
		time.sleep(0.1)

def devScript2():
	while True:
		if not sMCP.breakBeam_SENS.getVal():
			print("Break Beam Triggered....")
		else:
			print("Break Beam Not Triggered....")

def main():
	try:
		devScript()
		#devScript2()
		calibrate_horizontal_track()
		calibrate_vertical_track()
		#sendToHome()
		while True:
			checkException()
			IR_RUN_STATE()
	
	except KeyboardInterrupt:
		print("KeyboardInterrupt Triggered Killing the program...")
		sMotors.disableAllMotors()
	except mHaltException as lsObj:
		print(f"Stoppage Triggered By: {lsObj}")
		sMCP.estop_LED.turnOn()
	except Exception as e:
		sMCP.Error_LED.turnOn()
		sMotors.disableAllMotors()
		print(e)
		traceback.print_exc()
	finally:
		sMotors.disableAllMotors()
		garbageCollection()
		sys.exit(0)

if __name__ == "__main__":
	main()