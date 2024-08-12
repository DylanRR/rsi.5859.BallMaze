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

def test16():
  print("GPIO 16 - Step Pin Enabled")
  GPIO.output(STEP_PIN, GPIO.HIGH)
  time.sleep(1)
  print("GPIO 16 - Step Pin Disabled")
  GPIO.output(STEP_PIN, GPIO.LOW)
  time.sleep(5)

def test20():
  print("GPIO 20 - Enable Pin Enabled")
  GPIO.output(ENABLE_PIN, GPIO.HIGH)
  #time.sleep(5)
  #print("GPIO 20 - Enable Pin Disabled")
  #GPIO.output(ENABLE_PIN, GPIO.LOW)
  #time.sleep(5)

def test21():
  print("GPIO 21 - Direction Pin Enabled")
  GPIO.output(DIRECTION_PIN, GPIO.HIGH)
  time.sleep(5)
  print("GPIO 21 - Direction Pin Disabled")
  GPIO.output(DIRECTION_PIN, GPIO.LOW)
  time.sleep(5)


# Main function
def main():
  try:
    setup_gpio()
    test20()
    test16()
  finally:
    cleanup_gpio()

if __name__ == "__main__":
  main()