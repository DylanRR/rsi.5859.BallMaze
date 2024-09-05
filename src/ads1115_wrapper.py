import collections
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

class ADS_CHANNEL:
  def __init__(self, adsObj: ADS1115, channel, useSmoothing=False, bufferSize=10):
    self.__analogIn = AnalogIn(adsObj, channel)
    self.__bufferSize = bufferSize
    self.__buffer = None
    self.__smoothing = useSmoothing
    if self.__smoothing:
      self.__buffer = collections.deque(maxlen=self.__bufferSize)

  def close(self):
    self.__analogIn = None

  def __fillBuffer(self):
    if self.__buffer is not None:
      for i in range(self.__bufferSize):
        self.__buffer.append(self.__analogIn.value)

  def setSmoothing(self, useSmoothing, bufferSize=10):
    self.__smoothing = useSmoothing
    self.__bufferSize = bufferSize
    if self.__smoothing:
      if self.__buffer is None:
        self.__buffer = collections.deque(maxlen=self.__bufferSize)
      else:
        self.__buffer.clear()
        self.__buffer.maxlen = self.__bufferSize
    else:
      self.__buffer = None


  def getValue(self):
    val = self.__analogIn.value
    if self.__smoothing:
      self.__fillBuffer()
      val = sum(self.__buffer) / len(self.__buffer)
    return val
  




class MotorTracking:
  def __init__(self, adsObj: ADS1115, m1Tracking_channel, m2Tracking_channel, useSmoothing=False, bufferSize=10):
    self.__smoothing = useSmoothing
    self.__bufferSize = bufferSize

    self.__m1Tracking = ADS_CHANNEL(adsObj, m1Tracking_channel, useSmoothing, bufferSize)
    self.__m2Tracking = ADS_CHANNEL(adsObj, m2Tracking_channel, useSmoothing, bufferSize)
    self.__m1Max = 0
    self.__m2Max = 0
    self.__offset = 0
    self.__sweepLength = 37000
    self.__actOnDelta = 2000  # Minimum change in ADC value to act on
  
  def close(self):
    self.__m1Tracking.close()
    self.__m2Tracking.close()

  def calibrate(self):
    # Only call this function when you know that both pots are at their max values
    self.__m1Tracking.setSmoothing(True, 50)
    self.__m2Tracking.setSmoothing(True, 50)
    self.__m1Max = self.__m1Tracking.getValue()
    self.__m2Max = self.__m2Tracking.getValue()
    self.__m1Tracking.setSmoothing(self.__smoothing, self.__bufferSize)
    self.__m2Tracking.setSmoothing(self.__smoothing, self.__bufferSize)
    self.__offset = self.__m1Max - self.__m2Max

  def getM1Home(self):
    return (self.__m1Max - self.__sweepLength)
  def getM2Home(self):
    return (self.__m2Max - self.__sweepLength)
  
  # Returns the motor that needs to catch up
  # Lets say 1 is returned that means we need to stop motor 2 and move motor 1
  # We would than keep rechecking this function until 0 is returned
  # 0 means both motors are at the same position roughly and we can than move both motors

  # Current Direction: TRUE for UP, FALSE for DOWN
  def checkDeltaOffset(self, currentDirection):
    pass
