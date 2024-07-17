from gpiozero import Button, OutputDevice
import time
import os

ISR_LOCK = False
ISR_SOFT_LOCK = False

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
mDirection = OutputDevice(DIRECTION_PIN)
mStep = OutputDevice(STEP_PIN)
mEnable = OutputDevice(ENABLE_PIN, initial_value=True)  # Motor disabled initially

# Toggle motor function
def toggle_motor(enabled):
  mEnable.value = not enabled  # False to enable, True to disable
  print("Motor enabled" if enabled else "Motor disabled")

# Set motor direction function
def set_motor_direction(clockwise):
  mDirection.value = clockwise
  print(f"Motor direction set to {'clockwise' if clockwise else 'counter-clockwise'}")


# Generic Halt function
def halt(message):
	#ISR Locking Flags
	global ISR_LOCK
	ISR_LOCK = True
	print(f"\n{message}")
	toggle_motor(False)
	print("Exiting...")
	os._exit(1)

# E-STOP functions
def e_stop_halt():
  halt("E-Stop button pressed")

def left_ls_halt():
  halt("Left Halt Limit Switch triggered")

def right_ls_halt():
  halt("Right Halt Limit Switch triggered")

	
motorPause = True
motorDelay = None
encoderSpeed = None
trackHome = None
trackEnd = None
trackSteps = None
trackPosition = None

# Calibrate Track
trackHomeCalibrated = False
trackHomeFineCalibration = False
trackEndCalibrated = False
trackEndFineCalibration = False


def right_ls():
	#ISR Locking Flags
	global ISR_LOCK, ISR_SOFT_LOCK
	if ISR_LOCK:
		return
	ISR_LOCK = True
	ISR_SOFT_LOCK = True

	global trackHomeCalibrated, trackHome, trackPosition, trackHomeFineCalibration

	if not trackHomeCalibrated:
		trackPosition = 0
		move_motor(steps=100, clockwise=False)
		trackHomeCalibrated = True
	elif not trackHomeFineCalibration:
		move_motor(steps=20, clockwise=False)
		trackHome = 0
		trackHomeFineCalibration = True
		trackPosition = trackHome

	#ISR Unlocking Flags
	ISR_SOFT_LOCK = False
	ISR_LOCK = False

def left_ls():
	#ISR Locking Flags
	global ISR_LOCK, ISR_SOFT_LOCK
	if ISR_LOCK:
		return
	ISR_LOCK = True
	ISR_SOFT_LOCK = True

	global trackEndCalibrated, trackEnd, trackPosition, trackEndFineCalibration
	if not trackEndCalibrated:
		move_motor(steps=100, clockwise=True, delay=0.001)
		trackEndCalibrated = True
	elif not trackEndFineCalibration:
		move_motor(steps=20, clockwise=True, delay=0.001)
		trackEnd = trackPosition
		trackEndFineCalibration = True
	
	#ISR Unlocking Flags
	ISR_SOFT_LOCK = False
	ISR_LOCK = False
		

def calibrateTrack():
	#ISR Locking Flags
	global ISR_SOFT_LOCK
	ISR_SOFT_LOCK = True
	print("Calibrating Track...")
	global trackHomeCalibrated, trackEndCalibrated, trackPosition, trackSteps, trackHomeFineCalibration, trackEndFineCalibration
	set_motor_direction(True)
	while not trackHomeCalibrated:
		mStep.on()
		time.sleep(0.001)
		mStep.off()
		time.sleep(0.001)
	while not trackHomeFineCalibration:
		mStep.on()
		time.sleep(0.1)
		mStep.off()
		time.sleep(0.1)

	set_motor_direction(False)
	while not trackEndCalibrated:
		mStep.on()
		time.sleep(0.001)
		mStep.off()
		time.sleep(0.001)
		trackPosition += 1
	while not trackEndFineCalibration:
		mStep.on()
		time.sleep(0.1)
		mStep.off()
		time.sleep(0.1)
		trackPosition += 1
	
	trackSteps = trackEnd - trackHome
	print(f"Track Calibrated: Home: {trackHome}, End: {trackEnd}, Steps: {trackSteps}")
	ISR_SOFT_LOCK = False
    

# Move Motor
def move_motor(steps, clockwise, delay=0.01):
	global trackPosition
	toggle_motor(True)
	set_motor_direction(clockwise)
	for step in range(steps):
		mStep.on()
		time.sleep(delay)
		mStep.off()
		time.sleep(delay)
		trackPosition += -1 if clockwise else 1
		print(f"\rCurrent Position: {trackPosition}", end='', flush=True)
	print()

#Setting Interrupts
llsHalt.when_pressed = left_ls_halt
rlsHalt.when_pressed = right_ls_halt
btnHalt.when_deactivated = e_stop_halt
lls.when_pressed = left_ls
rls.when_pressed = right_ls

def main():
	print("Starting...")
	toggle_motor(True)
	calibrateTrack()
	move_motor(steps=round(trackSteps/2), clockwise=True, delay=0.001)
	toggle_motor(False)


if __name__ == "__main__":
	main()
