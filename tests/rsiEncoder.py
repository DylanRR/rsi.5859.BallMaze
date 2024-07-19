from gpiozero import Button
from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from digitalio import Direction, Pull
import digitalio

class rsiEncoder:
  def __init__(self, A_PIN, B_PIN, mcpObj):
    self.aPin = A_PIN
    self.bPin = B_PIN
    # Setup MCP23017 pins for the encoder
    self.__mcpObj = mcpObj
    self.encoderA = self.__mcpObj.get_pin(self.aPin)
    self.encoderB = self.__mcpObj.get_pin(self.bPin)
    self.__setupEncoderPins()
    self.__count = 0
    self.__last_encoderA_state = None
    self.__last_encoderB_state = None
    self.__direction = None   # True for CW, False for CCW
    self.__flipDirection = None
    self.__directionCount = 0
    self.__directionDelta = 2
    self.__prev_encoderA_val = 0
    self.__prev_encoderB_val = 0
    self.__IRS_LOCK = False
    

  def __setupEncoderPins(self):
    self.encoderA.direction = Direction.INPUT
    self.encoderA.pull = digitalio.Pull.UP
    self.encoderB.direction = Direction.INPUT
    self.encoderB.pull = digitalio.Pull.UP

  def getEncoderDirection(self):
    return self.__direction # True for CW, False for CCW
  
  def setIRSLock(self, lock):
    self.__IRS_LOCK = lock

  def __updateEncoderDirection(self):
    current_encoderA = self.encoderA.value
    current_encoderB = self.encoderB.value
    isCW = None
    # Determine the direction based on the change of state
    if self.__prev_encoderA_val == 0 and self.__prev_encoderB_val == 0:
      if current_encoderA == 1 and current_encoderB == 0:
        isCW = True
      elif current_encoderA == 0 and current_encoderB == 1:
        isCW = False
    elif self.__prev_encoderA_val == 1 and self.__prev_encoderB_val == 0:
      if current_encoderA == 1 and current_encoderB == 1:
        isCW = True
      elif current_encoderA == 0 and current_encoderB == 0:
        isCW = False
    elif self.__prev_encoderA_val == 1 and self.__prev_encoderB_val == 1:
      if current_encoderA == 0 and current_encoderB == 1:
        isCW = True
      elif current_encoderA == 1 and current_encoderB == 0:
        isCW = False
    elif self.__prev_encoderA_val == 0 and self.__prev_encoderB_val == 1:
      if current_encoderA == 0 and current_encoderB == 0:
        isCW = True
      elif current_encoderA == 1 and current_encoderB == 1:
        isCW = False
    self.__prev_encoderA_val = current_encoderA
    self.__prev_encoderB_val = current_encoderB
    
    if self.__flipDirection == None:
      self.__flipDirection = isCW
      return
    if self.__flipDirection == isCW:
      self.__directionCount += 1
    else:
      self.__directionCount = 0
      self.__flipDirection = isCW
    if self.__directionCount >= self.__directionDelta:
      self.__direction = self.__flipDirection
      self.__directionCount = 0


  def __testPrintDir(self):
    if self.__direction:
      print("CW")
    else:
      print("CCW")

  def isr(self):
    if self.__IRS_LOCK:
      return
    self.__updateEncoderDirection()
    self.__testPrintDir()
    
