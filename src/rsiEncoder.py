from gpiozero import Button
import board
import busio
from digitalio import Direction, Pull
import digitalio
import time
import threading

class rsiEncoder:
  def __init__(self, A_PIN, B_PIN):
    self.encoderA = Button(A_PIN, pull_up=True)
    self.encoderB = Button(B_PIN, pull_up=True)
    self.__direction = None   # True for CW, False for CCW
    self.__flipDirection = None
    self.__directionCount = 0
    self.__directionDelta = 3
    self.__prev_encoderA_val = 0
    self.__prev_encoderB_val = 0
    self.__IRS_LOCK = False

    self.__lastTrigger = None
    self.__encoderSpeed = 0
    self.__encoderTimeout = 250 # 250ms Default timeout
    self.encoderRunning = False

    #Create a thread to run the ISR
    self.__interrupt_thread = threading.Thread(target=self._wait_for_interrupt)
    self.__interrupt_thread.daemon = True
    self.__interrupt_thread.start()

  def _wait_for_interrupt(self):
    while True:
      if self.encoderA.is_pressed or self.encoderB.is_pressed:
        self.isr()

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

  def getLastTrigger(self):
    if self.__lastTrigger == None:
      self.__lastTrigger = time.time()
      return
    return self.__lastTrigger
  
  def getTimeout(self):
    return self.__encoderTimeout

  def __updateSpeed(self):
    if self.__lastTrigger == None:
      self.__lastTrigger = time.time()
      return
      
    timeDiff = (time.time() * 1000) - (self.__lastTrigger * 1000)

    if timeDiff > self.__encoderTimeout:
      self.__encoderSpeed = 0
      return
    
    # Dictionary mapping time thresholds to speeds
    speed_map = {
      15: 0,
      13: 10,
      11: 20,
      9: 30,
      7: 40,
      5: 50,
      4: 60,
      3: 65,
      2: 75,
      1: 85
    }

    # Iterate through the dictionary to find the appropriate speed
    for threshold, speed in sorted(speed_map.items(), reverse=True):
      if timeDiff > threshold:
        self.__encoderSpeed = speed
        break

    self.__lastTrigger = time.time()

  def isEncoderRunning(self):
    return self.encoderRunning

  def getSpeed(self):
    return self.__encoderSpeed
  
  def __testPrint(self):
    if self.__direction:
      print(f"CW, Speed: {self.getSpeed()}")
    else:
      print(f"CCW, Speed: {self.getSpeed()}")

  def getDirection(self):
    self.__updateEncoderDirection()
    return self.__direction
  


  def isr(self):
    if self.__IRS_LOCK:
     return
    self.__updateEncoderDirection()
    self.__updateSpeed()
    #self.__testPrint()
    
