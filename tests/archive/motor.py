from gpiozero import Button, OutputDevice
import time
import os

# Define GPIO pin numbers
DIRECTION_PIN = 21
STEP_PIN = 16
ENABLE_PIN = 20
HAULT_PIN = 4

# Initialize GPIO devices
direction = OutputDevice(DIRECTION_PIN)
step = OutputDevice(STEP_PIN)
enable = OutputDevice(ENABLE_PIN, initial_value=True)  # Motor disabled initially

# Toggle motor function
def toggle_motor(enabled):
    enable.value = not enabled  # False to enable, True to disable
    print("Motor enabled" if enabled else "Motor disabled")

# Move Motor
def move_motor(steps, clockwise, delay=0.01):  # Adjust default delay as needed
    direction.value = clockwise  # True for clockwise, False for counter-clockwise
    for _ in range(steps):
        step.on()
        time.sleep(delay)
        step.off()
        time.sleep(delay)
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
    haultBTN = Button(HAULT_PIN, pull_up=True, bounce_time=0.2)
    haultBTN.when_pressed = hault  # Use when_pressed for immediate response
    toggle_motor(True)  # Enable motor
    move_motor(steps=300, clockwise=True)
    time.sleep(1)
    move_motor(steps=300, clockwise=False)
    toggle_motor(False)  # Disable motor

if __name__ == "__main__":
    main()