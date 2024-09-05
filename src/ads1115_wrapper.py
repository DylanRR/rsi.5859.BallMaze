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
      val = sum(self.__buffer) // len(self.__buffer) # Average of the buffer using floor division
    return val
  




class MotorSync:
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
    self.__m1Tracking.setSmoothing(True, bufferSize=100)
    self.__m2Tracking.setSmoothing(True, bufferSize=100)
    self.__m1Max = self.__m1Tracking.getValue()
    self.__m2Max = self.__m2Tracking.getValue()
    self.__m1Tracking.setSmoothing(self.__smoothing, bufferSize=self.__bufferSize)
    self.__m2Tracking.setSmoothing(self.__smoothing, bufferSize=self.__bufferSize)
    self.__offset = self.__m1Max - self.__m2Max

  def getDistanceToHome(self):
    m1_value = self.__m1Tracking.getValue()
    home_position = self.__m1Max - self.__sweepLength
    distance_to_home = home_position - m1_value
    if distance_to_home <= 0:
        return 0.0
    return (distance_to_home / self.__sweepLength) * 100
  
  def getDistanceToMax(self):
    m1_value = self.__m1Tracking.getValue()
    distance_to_max = self.__m1Max - m1_value
    if distance_to_max <= 0:
        return 0.0
    return (distance_to_max / self.__sweepLength) * 100

  
  # Current Direction: TRUE for UP, FALSE for DOWN
  def getSyncInstructions(self, currentDirection):
    m1_value = self.__m1Tracking.getValue()
    m2_value = self.__m2Tracking.getValue()
    adjusted_m2_value = m2_value + self.__offset
    posDelta = m1_value - adjusted_m2_value
    percentage = (abs(posDelta) / self.__sweepLength) * 100
    if abs(posDelta) < self.__actOnDelta:
      return 0, percentage
    if (posDelta > 0 and currentDirection) or (posDelta < 0 and not currentDirection):
      #self.__debugPrint(2, m1_value, m2_value, adjusted_m2_value)
      return 2, percentage
    else:
      #self.__debugPrint(1, m1_value, m2_value, adjusted_m2_value)
      return 1, percentage
    
  def isDeSynced(self):
    m1_value = self.__m1Tracking.getValue()
    m2_value = self.__m2Tracking.getValue()
    adjusted_m2_value = m2_value + self.__offset
    posDelta = m1_value - adjusted_m2_value
    if abs(posDelta) > self.__actOnDelta:
      return True
    return False

    
    
  def __debugPrint(self, mNum, m1Val, m2Val, adjM2Val):
    print("M", mNum ," Needs Catchup   ", end='')
    print("M1 Real: ", m1Val, "   M2 Real: ", m2Val, "   Offset: ", self.__offset, "   M2 Adjusted: ", adjM2Val)