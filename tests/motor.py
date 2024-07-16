import RPi.GPIO as GPIO
from gpiozero import Button
from RpiMotorLib import RpiMotorLib
import time

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

# Move motor function
def move_motor(steps, direction, delay=0.04, verbose=False, steptype="Full"):
  motor = RpiMotorLib.A4988Nema(DIRECTION_PIN, STEP_PIN, (21,21,21), "DRV8825")
  motor.motor_go(
    clockwise=direction, 
    steptype=steptype, 
    steps=steps, 
    stepdelay=delay, 
    verbose=verbose
  )
	

# E-STOP function
def hault():
	print("E-Stop button pressed")
	toggle_motor(False)

# Main function
def main():
	try:
		setup_gpio()
		haultBTN = Button(HAULT_PIN, pull_up=True, bounce_time=0.2)
		haultBTN.when_deactivated = hault
		toggle_motor(True)
		move_motor(steps=10, direction=True)
		time.sleep(5)
		move_motor(steps=10, direction=False)
		toggle_motor(False)
	finally:
		cleanup_gpio()

if __name__ == "__main__":
	main()