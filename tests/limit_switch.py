from gpiozero import Button
import time

# Define GPIO pins to listen to and their corresponding names
pins = {
	18: "Left Initial Limit Switch",
	23: "Left Secondary Limit Switch",
	24: "Right Secondary Limit Switch",
	25: "Right Initial Limit Switch",
}

# Create a Button object for each pin
buttons = {pin: Button(pin, pull_up=True) for pin in pins}

# Define a callback function to handle button presses
def button_pressed(button):
	pin_name = pins[button.pin.number]
	print(f"{pin_name} triggered")

# Attach the callback function to the button press event for each Button object
for button in buttons.values():
	button.when_pressed = button_pressed

print("Listening for GPIO events. Press Ctrl+C to exit.")

try:
	# Keep the script running to listen for events
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print("Exiting...")