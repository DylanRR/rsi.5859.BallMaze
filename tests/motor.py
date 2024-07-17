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
	GPIO.output(ENABLE_PIN, GPIO.HIGH if enabled else GPIO.LOW)
	print("Motor enabled" if enabled else "Motor disabled")

# Move Motor
def move_motor(steps, clockwise, delay=1):
	GPIO.output(DIRECTION_PIN, GPIO.HIGH if clockwise else GPIO.LOW)
	print(f"Moving motor {'clockwise' if clockwise else 'counter-clockwise'}")
	for step in range(steps):
		GPIO.output(STEP_PIN, GPIO.LOW)
		time.sleep(delay)
		GPIO.output(STEP_PIN, GPIO.HIGH)
		time.sleep(delay)
		print(f"\rCurrent Step: {step + 1}/{steps}", end='', flush=True)
	print()  # Ensure to print a newline at the end to move the cursor to the next line

# E-STOP function
def hault():
	print("\nE-Stop button pressed")
	toggle_motor(True)
	print("Exiting...")
	os._exit(1)

# Main function
def main():
	try:
		setup_gpio()
		haultBTN = Button(HAULT_PIN, pull_up=True, bounce_time=0.2)
		haultBTN.when_deactivated = hault
		toggle_motor(False)
		move_motor(steps=300, clockwise=True, delay=.0005)
		time.sleep(5)
		move_motor(steps=300, clockwise=False, delay=.0005)
		toggle_motor(True)
	finally:
		cleanup_gpio()

if __name__ == "__main__":
	main()
