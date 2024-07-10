import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins to listen to and their corresponding names
pins = {
    18: "Left Initial Limit Switch",
    23: "Left Secondary Limit Switch",
    24: "Right Secondary Limit Switch",
    25: "Right Initial Limit Switch",
}

# Set up each pin as an input with a pull-up resistor
for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define a callback function to handle GPIO events
def gpio_callback(channel):
    pin_name = pins[channel]
    print(f"{pin_name} triggered")

# Add event detection for each pin
for pin in pins:
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