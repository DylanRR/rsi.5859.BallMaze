from gpiozero import Button
from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from digitalio import Direction, Pull
import digitalio

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP23017
mcp = MCP23017(i2c, address=0x20)


# Setup MCP23017 pins for the encoder
encoderA = mcp.get_pin(8)  # GPB0
encoderA.direction = Direction.INPUT
encoderA.pull = digitalio.Pull.UP

encoderB = mcp.get_pin(9)  # GPB1
encoderB.direction = Direction.INPUT
encoderB.pull = digitalio.Pull.UP

encoderZ = mcp.get_pin(10)  # GPB2
encoderZ.direction = Direction.INPUT
encoderZ.pull = digitalio.Pull.UP

# Enable interrupts for GPB0, GPB1, and GPB2
# mcp.interrupt_enable = 0x07  # 0b00000111
mcp.interrupt_enable = 0xFFFF
mcp.interrupt_configuration = 0x0000  # interrupt on any change
mcp.io_control = 0x44  # Interrupt as open drain and mirrored
mcp.clear_ints()  # Interrupts need to be cleared initially

# Configure interrupts to trigger on a change
mcp.interrupt_configuration = 0x00  # 0b00000000, compare against previous value

# Setup interrupt handling for INTB connected to GPIO #12 using gpiozero
intb_button = Button(12, pull_up=True)

# Global variables for encoder count and limits
count = 0

# Previous states of encoderA and encoderB to determine direction of rotation
last_encoderA_state = None
last_encoderB_state = None

def handle_interrupt():
  global count, last_encoderA_state, last_encoderB_state
  current_encoderA = encoderA.value
  current_encoderB = encoderB.value

	# Handle initial inturupt
  if last_encoderA_state is None or last_encoderB_state is None:
    last_encoderA_state = current_encoderA
    last_encoderB_state = current_encoderB
    return

  if last_encoderA_state != current_encoderA or last_encoderB_state != current_encoderB:
    # Determine direction based on A and B states
    if last_encoderA_state == 0 and current_encoderA == 1:
      if current_encoderB == 0:
          count += 1
      else:
          count -= 1
    elif last_encoderA_state == 1 and current_encoderA == 0:
      if current_encoderB == 1:
          count += 1
      else:
          count -= 1

  # Update last states for next interrupt
  last_encoderA_state = current_encoderA
  last_encoderB_state = current_encoderB
  
  # Print the current count
  print(f"Current count: {count}")

intb_button.when_pressed = handle_interrupt

# Keep the script running
input("Press enter to quit\n\n")