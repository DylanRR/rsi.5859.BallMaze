import RPi.GPIO as GPIO
import time

# Define GPIO pin to listen to
pin = 4

# Set up the pin as an input with a pull-up resistor
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define a callback function to handle GPIO events
def gpio_callback(channel):
    print("E-Stop button triggered")

# Add event detection for the pin
GPIO.add_event_detect(pin, GPIO.FALLING, callback=gpio_callback, bouncetime=200)

try:
    # Keep the script running to listen for events
    print("Listening for GPIO events. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")

# Clean up GPIO settings before exiting
GPIO.cleanup()