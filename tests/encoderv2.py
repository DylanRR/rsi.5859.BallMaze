from gpiozero import Button
import threading
import time
from functools import wraps

def run_in_thread(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    #print(f"Running function {fn.__name__} in a warpped thread")
    thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
    thread.start()
    return thread
  return wrapper

class Encoder:
  def __init__(self, leftPin, rightPin):
    self.__ISR_LOCK = False
    self.leftPin = Button(leftPin, pull_up=True)
    self.rightPin = Button(rightPin, pull_up=True)
    self.__value = 0
    self.__state = '00'
    self.direction = None
    self.__lastChangeTime = time.time()
    self.__timeout = 0.4
    self.__speed = 0
    self.__minSpeedDelta = 0.01
    self.__maxSpeedDelta = 0.001
    self.__speedSamples = []
    self.__numOfSpeedSamples = 100
    self.__threadLock = threading.Lock()
    
    self.leftPin.when_pressed = self.ISR
    self.rightPin.when_pressed = self.ISR
    self.leftPin.when_released = self.ISR
    self.rightPin.when_released = self.ISR

  def __del__(self):
    self.close()                                                    
  
  def close(self):  #TODO: Deal with open threads                                                    
    self.leftPin.close()                                                      # Close the left pin
    self.rightPin.close()                                                     # Close the right pin

  def ISR_LOCK(self, bool):
    self.__ISR_LOCK = bool

  @run_in_thread
  def ISR(self):
    if self.__ISR_LOCK:
      return
    p1 = self.leftPin.value                                               # Get the current left pin value
    p2 = self.rightPin.value                                              # Get the current right pin value
    newState = "{}{}".format(int(p1), int(p2))                                   # Create a new state based on the current pin values
    transitions = {                                                              # Dictionary holding possible transition keys and the actions to take on each key
      "00": { 
        "01": lambda: setattr(self, "direction", False),                         # Set direction to False on 00 -> 01 transition
        "10": lambda: setattr(self, "direction", True)},                         # Set direction to True on 00 -> 10 transition
      "01": {
        "11": lambda: setattr(self, "direction", False),                         # Set direction to False on 01 -> 11 transition
        "00": lambda: self.__decrement_value() if self.direction else None},     # Decrement value if direction is True on 01 -> 00
      "10": {
        "11": lambda: setattr(self, "direction", True),                          # Set direction to True on 10 -> 11 transition
        "00": lambda: self.__increment_value() if not self.direction else None}, # Increment value if direction is False on 10 -> 00
      "11": {
        "01": lambda: setattr(self, "direction", True),                                             # Set direction to True on 11 -> 01 transition
        "10": lambda: setattr(self, "direction", False),                                            # Set direction to False on 11 -> 10 transition
        "00": lambda: self.__increment_value() if not self.direction else self.__decrement_value()} # Increment or decrement based on direction on 11 -> 00
    }
    action = transitions.get(self.__state, {}).get(newState, lambda: None)      # Get the action to perform based on the current and new state, default to doing nothing if transition not defined
    action()                                                                    # Execute the action
    self.__state = newState                                                     # Update the current state to the new state
    self.__calcSpeed()

  def __increment_value(self):
    self.__value += 1
    self.__lastChangeTime = time.time()

  def __decrement_value(self):
    self.__value -= 1
    self.__lastChangeTime = time.time()

  def __checkTimeout(self):
    if (time.time() - self.__lastChangeTime) > self.__timeout:
      self.direction = None
      self.__value = 0
      self.__speed = 0
      self.__speedSamples.clear()

  def __calcSpeed(self):
    with self.__threadLock:
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
    

  def getSpeed(self):
    with self.__threadLock:
      self.__checkTimeout()
      return self.__speed
  
  def isEncoderRunning(self):
    with self.__threadLock:
      self.__checkTimeout()
      return True if self.direction is not None else False

  def getValue(self):
    self.__checkTimeout()
    return self.__value
  
  def hasDirChanged(self, dirValue) -> bool:
    return False if dirValue == self.direction else True