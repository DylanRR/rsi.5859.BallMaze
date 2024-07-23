from gpiozero import Button
import threading

class Encoder:

  def __init__(self, leftPin, rightPin):
    self.leftPin = Button(leftPin)
    self.rightPin = Button(rightPin)
    self.value = 0
    self.state = '00'
    self.direction = None

    # Initialize the lock for thread synchronization
    self.__ISR_LOCK = threading.Lock()

    # Create a thread to run the ISR
    self.__interrupt_thread = threading.Thread(target=self._wait_for_interrupt)
    self.__interrupt_thread.daemon = True
    self.__interrupt_thread.start()

  def _wait_for_interrupt(self):
    while True:
      if self.leftPin.is_pressed or self.rightPin.is_pressed:
        with self.__ISR_LOCK:
          self.ISR()

  def ISR(self):
    p1 = self.leftPin.is_pressed
    p2 = self.rightPin.is_pressed
    newState = "{}{}".format(int(p1), int(p2))

    if self.state == "00": # Resting position
      if newState == "01": # Turned right 1
        self.direction = "R"
      elif newState == "10": # Turned left 1
        self.direction = "L"

    elif self.state == "01": # R1 or L3 position
      if newState == "11": # Turned right 1
        self.direction = "R"
      elif newState == "00": # Turned left 1
        if self.direction == "L":
          self.value = self.value - 1

    elif self.state == "10": # R3 or L1
      if newState == "11": # Turned left 1
        self.direction = "L"
      elif newState == "00": # Turned right 1
        if self.direction == "R":
          self.value = self.value + 1

    else: # self.state == "11"
      if newState == "01": # Turned left 1
        self.direction = "L"
      elif newState == "10": # Turned right 1
        self.direction = "R"
      elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
        if self.direction == "L":
          self.value = self.value - 1
        elif self.direction == "R":
          self.value = self.value + 1

    self.state = newState

  def getValue(self):
      return self.value