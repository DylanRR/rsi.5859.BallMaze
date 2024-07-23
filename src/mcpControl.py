from gpiozero import Button
from adafruit_mcp230xx.mcp23017 import MCP23017
import digitalio

class mcpInputInterruptPin:
  def __init__(self, pin, mcpObj: MCP23017, pull_up=digitalio.Pull.UP ,direction=digitalio.Direction.INPUT):
    self.pin = pin
    self.__mcpObj = mcpObj
    self.__switch = self.__mcpObj.get_pin(pin)
    self.__switch.direction = direction
    self.__switch.pull = pull_up
    self.__mcpObj.interrupt_enable = 1 << self.pin
    self.__lockedOut = False
    self.__firstCalibration = False
    self.__secondCalibration = False
    

  def __del__(self):
    self.__mcpObj.interrupt_enable &= ~(1 << self.pin)  # Disable interrupt for the specific pin
    self.__switch.pull = None  # Remove pull-up/down resistor

  def nonCalISR(self):
    pass  # Placeholder for the non-calibration ISR

  def __irs(self):
    if self.__lockedOut:
      return

    if not self.__firstCalibration:
      self.__firstCalibration = True
      self.__lockedOut = True
      return

    if not self.__secondCalibration:
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
    flag = self.__mcpObj.interrupt_flag
    if flag & (1 << self.pin):
      self.__irs()
      self.__mcpObj.clear_ints()  # Clear the interrupt flag

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