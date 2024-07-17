from gpiozero import Button, OutputDevice
import time
import os

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
		
def set_motor_direction(clockwise):
  mDirection.value = clockwise
  print(f"Motor direction set to {'clockwise' if clockwise else 'counter-clockwise'}")


# Generic Halt function
def halt(message):
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
trackEndCalibrated = False

def right_ls():
	global trackHomeCalibrated, trackHome, trackPosition
	if not trackHomeCalibrated:
		trackPosition = 0
		move_motor(steps=20, clockwise=False)
		trackHome = 0
		trackHomeCalibrated = True
	print(f"Setting track position to adjusted home:{trackHome}")
	trackPosition = trackHome

def left_ls():
	global trackEndCalibrated, trackEnd, trackPosition
	if not trackEndCalibrated:
		move_motor(steps=20, clockwise=True)
		trackEnd = trackPosition - 20
		trackEndCalibrated = True
		

def calibrateTrack():
	print("Calibrating Track...")
	global trackHomeCalibrated, trackEndCalibrated, trackPosition, trackSteps
	toggle_motor(True) # May need to change to False
	set_motor_direction(True)
	while not trackHomeCalibrated:
		mStep.on()
		time.sleep(0.001)
		mStep.off()
		time.sleep(0.001)
	set_motor_direction(False) # May need to change to False
	toggle_motor(True)
	while not trackEndCalibrated:
		mStep.on()
		time.sleep(0.001)
		mStep.off()
		time.sleep(0.001)
		trackPosition += 1
	
	trackSteps = trackEnd - trackHome
	toggle_motor(False)
	print(f"Track Calibrated: Home: {trackHome}, End: {trackEnd}, Steps: {trackSteps}")
    

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
		if clockwise:
			trackPosition -= 1
		else:
			trackPosition += 1
		print(f"\rCurrent Position: {trackPosition}", end='', flush=True)
	print()
	toggle_motor(False)


llsHalt.when_pressed = left_ls_halt
rlsHalt.when_pressed = right_ls_halt
btnHalt.when_deactivated = e_stop_halt
lls.when_pressed = left_ls
rls.when_pressed = right_ls
def main():
	try:
		print("Starting...")
		calibrateTrack()
		move_motor(steps=round(trackSteps/2), clockwise=True, delay=0.001)
	finally:
		toggle_motor(False)

if __name__ == "__main__":
	main()
