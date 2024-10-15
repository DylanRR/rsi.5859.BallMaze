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
        self.__buffer = collections.deque(self.__buffer, maxlen=self.__bufferSize)
    else:
      self.__buffer = None


  def getValue(self):
    val = self.__analogIn.value
    if self.__smoothing:
      self.__fillBuffer()
      val = sum(self.__buffer) // len(self.__buffer) # Average of the buffer using floor division
    return val
  


#NOTE: Before we were not using smoothing on our get values we introduce smoothing in when we calibrate.

class MotorSync:
  def __init__(self, adsObj: ADS1115, m1Tracking_channel, m2Tracking_channel, useSmoothing=False, bufferSize=10):
    self.__m1Tracking = ADS_CHANNEL(adsObj, m1Tracking_channel, useSmoothing, bufferSize)
    self.__m2Tracking = ADS_CHANNEL(adsObj, m2Tracking_channel, useSmoothing, bufferSize)
    self.__m1Max = 0
    self.__m2Max = 0
    self.__offset = 0
    self.__actOnDelta = 2000  # Minimum change in ADC value to act on
    self.__fineSyncDelta = 25  # Minimum change in ADC value to be considered finely synced
    
  
  def close(self):
    self.__m1Tracking.close()
    self.__m2Tracking.close()

  def calibrate(self):
    # Only call this function when you know that both pots are at their max values
    self.__m1Tracking.setSmoothing(True, bufferSize=100)
    self.__m2Tracking.setSmoothing(True, bufferSize=100)
    self.__m1Max = self.__m1Tracking.getValue()
    self.__m2Max = self.__m2Tracking.getValue()
    self.__offset = self.__m1Max - self.__m2Max
    self.__m1Tracking.setSmoothing(True)
    self.__m2Tracking.setSmoothing(True)

    
  def getReSyncDirection(self):
    m1_value = self.__m1Tracking.getValue()
    m2_value = self.__m2Tracking.getValue()
    adjusted_m2_value = m2_value + self.__offset
    posDelta = m1_value - adjusted_m2_value
    if posDelta > 0:
      return False
    else:
      return True
    
  def isDeSynced(self):
    m1_value = self.__m1Tracking.getValue()
    m2_value = self.__m2Tracking.getValue()
    adjusted_m2_value = m2_value + self.__offset
    posDelta = m1_value - adjusted_m2_value
    if abs(posDelta) > self.__actOnDelta:
      return True
    return False
  
  def isFineSynced(self):
    m1_value = self.__m1Tracking.getValue()
    m2_value = self.__m2Tracking.getValue()
    adjusted_m2_value = m2_value + self.__offset
    posDelta = m1_value - adjusted_m2_value
    if abs(posDelta) < self.__fineSyncDelta:
      return True
    return False