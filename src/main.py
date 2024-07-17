import RPi.GPIO as GPIO
from gpiozero import Button
from RpiMotorLib import RpiMotorLib
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

llsHalt = Button(LEFT_SECONDARY_LIMIT_SWITCH, pull_up=True)
rlsHalt = Button(RIGHT_SECONDARY_LIMIT_SWITCH, pull_up=True)
btnHalt = Button(HALT_PIN, pull_up=True, bounce_time=0.2)



# Define other motor parameters
motor_type = 'A4988'
motor_mode = [-1,-1,-1]
motor_pins = (DIRECTION_PIN, STEP_PIN)
motor = RpiMotorLib.A4988Nema(DIRECTION_PIN, STEP_PIN, motor_mode, motor_type)

# Initialize GPIO
def setup_gpio():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DIRECTION_PIN, GPIO.OUT)
	GPIO.setup(STEP_PIN, GPIO.OUT)
	GPIO.setup(ENABLE_PIN, GPIO.OUT)
	print("GPIO setup complete")

# Cleanup GPIO
def cleanup_gpio():
	GPIO.cleanup()
	print("GPIO cleanup complete")

# Toggle motor function
def toggle_motor(enabled):
	GPIO.output(ENABLE_PIN, GPIO.LOW if enabled else GPIO.HIGH)
	print("Motor enabled" if enabled else "Motor disabled")

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

def setup_eStopInterrupts():
	llsHalt.when_pressed = left_ls_halt
	rlsHalt.when_pressed = right_ls_halt
	btnHalt.when_deactivated = e_stop_halt
	print("E-Stop setup complete")
	
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
		move_motor(steps=20, clockwise=False)
		trackHome = 0
		trackPosition = 0
		trackHomeCalibrated = True

def left_ls():
	global trackEndCalibrated, trackEnd, trackPosition
	if not trackEndCalibrated:
		move_motor(steps=20, clockwise=True)
		trackEnd = trackPosition - 20
		trackEndCalibrated = True
		


def setup_LSInterrupts():
	Button(LEFT_INITIAL_LIMIT_SWITCH, pull_up=True).when_activated = left_ls
	Button(RIGHT_INITIAL_LIMIT_SWITCH, pull_up=True).when_activated = right_ls
	print("Limit Switch setup complete")
	


def calibrateTrack():
	print("Calibrating Track...")
	global trackHomeCalibrated, trackEndCalibrated, trackPosition
	toggle_motor(True)
	GPIO.output(DIRECTION_PIN, GPIO.HIGH)
	while not trackHomeCalibrated:
		GPIO.output(STEP_PIN, GPIO.LOW)
		time.sleep(0.01)
		GPIO.output(STEP_PIN, GPIO.HIGH)
		time.sleep(0.01)
	GPIO.output(DIRECTION_PIN, GPIO.Low)
	while not trackEndCalibrated:
		GPIO.output(STEP_PIN, GPIO.LOW)
		time.sleep(0.01)
		GPIO.output(STEP_PIN, GPIO.HIGH)
		time.sleep(0.01)
		trackPosition += 1
	trackSteps = trackEnd - trackHome
	toggle_motor(False)
	print(f"Track Calibrated: Home: {trackHome}, End: {trackEnd}, Steps: {trackSteps}")
    

# Move Motor
def move_motor(steps, clockwise, delay=0.01):
	GPIO.output(DIRECTION_PIN, GPIO.HIGH if clockwise else GPIO.LOW)
	for step in range(steps):
		GPIO.output(STEP_PIN, GPIO.LOW)
		time.sleep(delay)
		GPIO.output(STEP_PIN, GPIO.HIGH)
		time.sleep(delay)


  

def main():
	llsHalt.when_pressed = left_ls_halt
	rlsHalt.when_pressed = right_ls_halt
	btnHalt.when_deactivated = e_stop_halt
	setup_gpio()
	#setup_eStopInterrupts()
	setup_LSInterrupts()
	try:
		print("Starting...")
		calibrateTrack()
	finally:
		toggle_motor(False)
		cleanup_gpio()

if __name__ == "__main__":
	main()
