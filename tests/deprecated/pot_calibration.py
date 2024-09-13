import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time  # Required for debugging

# Predefined GPIO pin numbers for chip select
CE0_PIN = board.D8  # GPIO pin for CE0
CE1_PIN = board.D7  # GPIO pin for CE1

# Predefined number of steps for a full sweep
SWEEP_LENGTH = 10000

class MotorTracking:
  def __init__(self, motor1PotChannel, motor2PotChannel, chipSelect=CE0_PIN):
    self.__spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    self.__cs = digitalio.DigitalInOut(chipSelect)
    self.__cs.direction = digitalio.Direction.OUTPUT
    self.__mcp = MCP.MCP3008(self.__spi, self.__cs)
    self.__motor1Pot = AnalogIn(self.__mcp, motor1PotChannel)
    self.__motor2Pot = AnalogIn(self.__mcp, motor2PotChannel)
    self.__m1RelativePosition = 0
    self.__m2RelativePosition = 0
    self.__m1RelativeMax = 0
    self.__m2RelativeMax = 0
    self.__m1RelativeMin = 0
    self.__m2RelativeMin = 0
    self.__actOnDelta = 50  # Minimum change in ADC value to act on
  
  def __del__(self):
    self.close()

  def close(self):
    if hasattr(self, '__spi') and self.__spi:
      self.__spi.deinit()
    if hasattr(self, '__cs') and self.__cs:
      self.__cs.deinit()

  # Only call this function when you know that both pots are at their max values
  def __setRelativeMinMax(self, motor1Max, motor2Max): #TODO: Add a check for RelativeMax > RelativeMin and not negative
    self.__m1RelativeMax = motor1Max
    self.__m2RelativeMax = motor2Max
    self.__m1RelativeMin = motor1Max - SWEEP_LENGTH
    self.__m2RelativeMin = motor2Max - SWEEP_LENGTH

  def __mapValue(self, value, from_min, from_max, to_min, to_max):
    return (value - from_min) * (to_max - to_min) // (from_max - from_min) + to_min
  
  def __mapM1Value(self, value):
    return self.__mapValue(value, self.__m1RelativeMin, self.__m1RelativeMax, 0, SWEEP_LENGTH)
  
  def __mapM2Value(self, value):
    return self.__mapValue(value, self.__m2RelativeMin, self.__m2RelativeMax, 0, SWEEP_LENGTH)

  def __getMotor1PotValue(self):
    return self.__motor1Pot.value
  
  def __getMotor2PotValue(self):
    return self.__motor2Pot.value
  
  def calibrate(self):
    # Move the motors to their max values
    m1TempVal = self.__getMotor1PotValue()
    m2TempVal = self.__getMotor2PotValue()
    self.__setRelativeMinMax(m1TempVal, m2TempVal)
    self.__m1RelativePosition = self.__mapM1Value(m1TempVal)
    self.__m2RelativePosition = self.__mapM2Value(m2TempVal)

  def __updateRelativePosition(self):
    self.__m1RelativePosition = self.__mapM1Value(self.__getMotor1PotValue())
    self.__m2RelativePosition = self.__mapM2Value(self.__getMotor2PotValue())
  
  # Returns the motor that needs to catch up
  # Lets say 1 is returned that means we need to stop motor 2 and move motor 1
  # We would than keep rechecking this function until 0 is returned
  # 0 means both motors are at the same position roughly and we can than move both motors

  # Current Direction: TRUE for UP, FALSE for DOWN
  def checkForDeltaOffset(self, currentDirection):
    self.__updateRelativePosition()
    posDelta = self.__m1RelativePosition - self.__m2RelativePosition
    if abs(posDelta) < self.__actOnDelta:
      return 0
    if (posDelta > 0 and currentDirection) or (posDelta < 0 and not currentDirection):
      return 2
    else:
      return 1

      