import RPi.GPIO as GPIO
from gpiozero import Button
from RpiMotorLib import RpiMotorLib
import time
import os

# Define GPIO pin numbers
DIRECTION_PIN = 21
STEP_PIN = 16
ENABLE_PIN = 20
HAULT_PIN = 4

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

# Cleanup GPIO
def cleanup_gpio():
	GPIO.cleanup()

# Toggle motor function
def toggle_motor(enabled):
	GPIO.output(ENABLE_PIN, GPIO.LOW if enabled else GPIO.HIGH)
	print("Motor enabled" if enabled else "Motor disabled")

# Move Motor
def move_motor(steps, clockwise, delay=0.01):  # Adjust default delay as needed
	direction = clockwise  # True for clockwise, False for counter-clockwise
	motor.motor_go(direction, 'Full', steps, delay, False, .05)
	print(f"Moving motor {'clockwise' if clockwise else 'counter-clockwise'}")
	print(f"Completed {steps} steps.")

# E-STOP function
def hault():
	print("\nE-Stop button pressed")
	toggle_motor(False)
	print("Exiting...")
	os._exit(1)

# Main function
def main():
	try:
		setup_gpio()
		haultBTN = Button(HAULT_PIN, pull_up=True, bounce_time=0.2)
		haultBTN.when_deactivated = hault
		toggle_motor(True)
		move_motor(steps=300, clockwise=True)
		time.sleep(1)
		move_motor(steps=300, clockwise=False)
	finally:
		toggle_motor(False)
		cleanup_gpio()

if __name__ == "__main__":
	main()
