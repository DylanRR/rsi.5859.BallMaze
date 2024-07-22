import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
from gpiozero import Button
import signal
from rsiEncoder import rsiEncoder
import threading
from time import sleep
from rsiStepMotor import rsiStepMotor

INTB_PIN = 12
MCP_ENCODER_A_PIN = 8
MCP_ENCODER_B_PIN = 9


# Initialize I2C bus and MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)

# Set up GPIO 12 as the interrupt pin using gpiozero

# Enable interrupts for GPB0, GPB1, and GPB2
# mcp.interrupt_enable = 0x07  # 0b00000111
mcp.interrupt_enable = 0xFFFF
mcp.interrupt_configuration = 0x0000  # interrupt on any change
mcp.io_control = 0x44  # Interrupt as open drain and mirrored
mcp.clear_ints()  # Interrupts need to be cleared initially
# Configure interrupts to trigger on a change
mcp.interrupt_configuration = 0x00  # 0b00000000, compare against previous value

# Setup interrupt handling for INTB connected to GPIO #12 using gpiozero
INTB_PIN = 12
intb_pin = Button(INTB_PIN, pull_up=True)

# Setup the encoder
encoder1 = rsiEncoder(MCP_ENCODER_A_PIN, MCP_ENCODER_B_PIN, mcp)

def start_isr_thread():
  threading.Thread(target=encoder1.isr).start()

intb_pin.when_pressed = start_isr_thread

while(True):
  print("loop")
  sleep(2)

# Keep the script running
input("Press enter to quit\n\n")
# Cleanup
intb_pin.close()