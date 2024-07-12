from gpiozero import Button
from signal import pause

# Define GPIO pin to listen to
pin = 4

# Set up the pin as a Button, assuming the button is Normally Closed (NC)
# and inverts the logic by setting pull_up=False
button = Button(pin, pull_up=True, bounce_time=0.2)

# Define a callback function to handle button press
def on_press():
	print("E-Stop button pressed")

# Attach the callback function to the button press event
button.when_deactivated = on_press

print("Listening for button press. Press Ctrl+C to exit.")
pause()  # Keep the program running