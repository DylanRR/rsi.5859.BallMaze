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

###########SETUP INTERRUPT FOR ENCODER################

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
direction = None   # True for CW, False for CCW
flipDirection = None
directionCount = 0
directionDelta = 2
prev_encoderA_val = 0
prev_encoderB_val = 0

def handle_interrupt():
  global direction, flipDirection, directionCount
  isCW = getEncoderDirection()
  if flipDirection == None:
    flipDirection = isCW
    return
  
  if flipDirection == isCW:
    directionCount += 1
  else:
    directionCount = 0
    flipDirection = isCW

  if directionCount >= directionDelta:
    direction = flipDirection
    directionCount = 0
    printDirection()



def getEncoderDirection():
  global prev_encoderA_val, prev_encoderB_val
  current_encoderA = encoderA.value
  current_encoderB = encoderB.value
  # Initialize isCW to None; it will be updated based on the direction
  isCW = None
  # Determine the direction based on the change of state
  if prev_encoderA_val == 0 and prev_encoderB_val == 0:
    if current_encoderA == 1 and current_encoderB == 0:
      isCW = True
    elif current_encoderA == 0 and current_encoderB == 1:
      isCW = False
  elif prev_encoderA_val == 1 and prev_encoderB_val == 0:
    if current_encoderA == 1 and current_encoderB == 1:
      isCW = True
    elif current_encoderA == 0 and current_encoderB == 0:
      isCW = False
  elif prev_encoderA_val == 1 and prev_encoderB_val == 1:
    if current_encoderA == 0 and current_encoderB == 1:
      isCW = True
    elif current_encoderA == 1 and current_encoderB == 0:
      isCW = False
  elif prev_encoderA_val == 0 and prev_encoderB_val == 1:
    if current_encoderA == 0 and current_encoderB == 0:
      isCW = True
    elif current_encoderA == 1 and current_encoderB == 1:
      isCW = False


  prev_encoderA_val = current_encoderA
  prev_encoderB_val = current_encoderB
  return isCW

def printDirection():
  global direction
  if direction:
    print("CW")
  else:
    print("CCW")


intb_button.when_pressed = handle_interrupt

# Keep the script running
input("Press enter to quit\n\n")