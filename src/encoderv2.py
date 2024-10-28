from gpiozero import Button
import threading
import time
from functools import wraps

def run_in_thread(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    #print(f"Running function {fn.__name__} in a wrapped thread")
    thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
    thread.start()
    return thread
  return wrapper

class Encoder:
  def __init__(self, leftPin, rightPin):
    self.__ISR_LOCK = False
    self.leftPin = Button(leftPin, pull_up=True)
    self.rightPin = Button(rightPin, pull_up=True)
    self.__timeout = 0.25
    self.__encoderRunning = False
    self.__lastChangeTime = time.time()

    self.__oldP1 = 0
    self.__oldP2 = 0
    self.counter = 0

    self.leftPin.when_pressed = self.ISR5
    self.rightPin.when_pressed = self.ISR5
    self.leftPin.when_released = self.ISR5
    self.rightPin.when_released = self.ISR5



    self.__minSpeedDelta = 0.01
    self.__maxSpeedDelta = 0.001
    self.__speedSamples = []
    self.__numOfSpeedSamples = 100
    self.__speed = 0

  def __del__(self):
    self.close()                                                    
  
  def close(self):                                                  
    self.leftPin.close()                                                      # Close the left pin
    self.rightPin.close()                                                     # Close the right pin

  def ISR_LOCK(self, bool):
    self.__ISR_LOCK = bool

  @run_in_thread
  def ISR6(self):
    if self.__ISR_LOCK:
      return
    p1 = self.leftPin.value
    p2 = self.rightPin.value
    if self.__oldP1 == p1 and self.__oldP2 == p2:
      return
    
    if self.__oldP2 != p2:
      if(self.__oldP1 == 1):
        if p2 == 0:
          self.counter -= 1
        else:
          self.counter += 1
    self.__oldP1 = p1
    self.__oldP2 = p2

    if self.counter > 5:
      self.counter = 5
    elif self.counter < -5:
      self.counter = -5

  @run_in_thread
  def ISR5(self):
    if self.__ISR_LOCK:
      return
    p1 = self.leftPin.value
    p2 = self.rightPin.value
    if self.__oldP1 == p1 and self.__oldP2 == p2:
      return
  
  # Determine direction based on state transition
    if self.__oldP1 == 0 and self.__oldP2 == 0:
      if p1 == 1 and p2 == 0:
        self.counter += 1
      elif p1 == 0 and p2 == 1:
        self.counter -= 1
    elif self.__oldP1 == 1 and self.__oldP2 == 0:
      if p1 == 1 and p2 == 1:
        self.counter += 1
      elif p1 == 0 and p2 == 0:
        self.counter -= 1
    elif self.__oldP1 == 1 and self.__oldP2 == 1:
      if p1 == 0 and p2 == 1:
        self.counter += 1
      elif p1 == 1 and p2 == 0:
        self.counter -= 1
    elif self.__oldP1 == 0 and self.__oldP2 == 1:
      if p1 == 0 and p2 == 0:
        self.counter += 1
      elif p1 == 1 and p2 == 1:
        self.counter -= 1

    if self.counter > 5:
      self.counter = 5
    elif self.counter < -5:
      self.counter = -5
    
    self.__oldP1 = p1
    self.__oldP2 = p2
    
    self.__lastChangeTime = time.time()
    self.__calcSpeed()


  def __calcSpeed(self):
    timeDiff = time.time() - self.__lastChangeTime
    if timeDiff < self.__timeout:
      # Calculate a normalized time difference within the operational range
      normalized_timeDiff = (timeDiff - self.__minSpeedDelta) / (self.__maxSpeedDelta - self.__minSpeedDelta)
      normalized_timeDiff = max(0, min(normalized_timeDiff, 1))  # Ensure it's between 0 and 1

      # Invert the formula to increase speed value as normalized_timeDiff increases
      tempSpeed = round(1 + (99 * normalized_timeDiff))  # Adjusted formula
      tempSpeed = max(1, min(tempSpeed, 100))  # Ensure speed is within the expected range

      self.__speedSamples.append(tempSpeed)
      if len(self.__speedSamples) > self.__numOfSpeedSamples:
        avg = sum(self.__speedSamples) / len(self.__speedSamples)
        avg = round(avg)
        avg = max(1, min(avg, 100))
        self.__speed = avg
        self.__speedSamples.clear()
    else:
      self.__speed = 0
      self.__speedSamples.clear()

  def __checkTimeout(self):
    if (time.time() - self.__lastChangeTime) > self.__timeout:
      self.__encoderRunning = False
      self.counter = 0
      self.__speed = 0
    else:
      self.__encoderRunning = True
  
  def getSpeed(self):
    self.__checkTimeout()
    return self.__speed

  def getDirection(self):
    self.__checkTimeout()
    return True if self.counter > 0 else False

  def isEncoderRunning(self):
    self.__checkTimeout()
    return self.__encoderRunning
  
  def hasDirChanged(self, dirValue) -> bool:
    return False if dirValue == self.getDirection() else True