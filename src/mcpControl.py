from gpiozero import Button
from adafruit_mcp230xx.mcp23017 import MCP23017
import digitalio

class mcpInputInterruptPin:
  def __init__(self, pin, mcpObj: MCP23017, pull_up=digitalio.Pull.UP ,direction=digitalio.Direction.INPUT):
    self.pin = pin
    self.__mcpObj = mcpObj
    # Enable interrupt for the specific pin without overwriting other settings
    current_interrupts = self.__mcpObj.interrupt_enable
    self.__mcpObj.interrupt_enable = current_interrupts | (1 << self.pin)
    self.__switch = self.__mcpObj.get_pin(pin)
    self.__switch.direction = direction
    self.__switch.pull = pull_up
    self.__lockedOut = False
    self.__firstCalibration = False
    self.__secondCalibration = False
    

  def __del__(self):
    self.__mcpObj.interrupt_enable &= ~(1 << self.pin)  # Disable interrupt for the specific pin
    self.__switch.pull = None  # Remove pull-up/down resistor

  def nonCalISR(self):
    pass  # Placeholder for the non-calibration ISR

  def __isr(self):
    print(f"ISR running on Pin {self.pin}")
    if self.__lockedOut:
      return
    print("ISR not locked out")

    if not self.__firstCalibration:
      print("First Calibration")
      self.__firstCalibration = True
      self.__lockedOut = True
      return

    if not self.__secondCalibration:
      print("Second Calibration")
      self.__secondCalibration = True
      self.__lockedOut = True
      return

    self.nonCalISR()

  def getFirstCalibration(self) -> bool:
    return self.__firstCalibration

  def getSecondCalibration(self) -> bool:
    return self.__secondCalibration

  def setLockedOut(self, lock: bool):
    self.__lockedOut = lock

  def handle_interrupt(self):
    self.__isr()

class mcpOutputPin:
  def __init__(self, pin, mcpObj: MCP23017, pull_up=False):
    self.pin = pin
    self.__mcpObj = mcpObj
    self.__pin = self.__mcpObj.get_pin(pin)
    self.__pin.direction = digitalio.Direction.OUTPUT
    if pull_up:
      self.__pin.pull = digitalio.Pull.UP

  def __del__(self):
    self.__pin.value = False # Setting Pin to known value

  def setPin(self, state: bool):
    self.__pin.value = state

  def getPin(self) -> bool:
    return self.__pin.value