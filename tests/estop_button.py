import RPi.GPIO as GPIO
import time

# Set the pin numbering mode
GPIO.setmode(GPIO.BCM)  # or GPIO.BOARD

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
         # Print the current state of the pin for debugging
        pin_state = GPIO.input(pin)
        print(f"GPIO pin {pin} state: {pin_state}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")

# Clean up GPIO settings before exiting
GPIO.cleanup()