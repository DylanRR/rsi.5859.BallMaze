from gpiozero import Button
import threading
import time

class rsiEncoder:
  def __init__(self, A_PIN, B_PIN):
    self.encoderA = Button(A_PIN, pull_up=True)
    self.encoderB = Button(B_PIN, pull_up=True)
    self.__direction = None   # True for CW, False for CCW
    self.__prev_encoderA_val = 0
    self.__prev_encoderB_val = 0
    self.__IRS_LOCK = threading.Lock()

    self.__lastTrigger = time.time()
    self.__encoderSpeed = 0
    self.encoderRunning = True

    # Create a thread to run the ISR
    self.__interrupt_thread = threading.Thread(target=self._wait_for_interrupt)
    self.__interrupt_thread.daemon = True
    self.__interrupt_thread.start()

  def _wait_for_interrupt(self):
    while self.encoderRunning:
      if self.encoderA.is_pressed or self.encoderB.is_pressed:
        with self.__IRS_LOCK:
          self.ISR()
      time.sleep(0.001)  # Small delay to prevent CPU hogging

  def ISR(self):
    current_time = time.time()
    if self.__lastTrigger is not None:
      time_diff = current_time - self.__lastTrigger
      if time_diff > 0:
        self.__encoderSpeed = 1 / time_diff
    self.__lastTrigger = current_time

    encoderA_val = self.encoderA.is_pressed
    encoderB_val = self.encoderB.is_pressed

    if encoderA_val != self.__prev_encoderA_val or encoderB_val != self.__prev_encoderB_val:
      if encoderA_val == encoderB_val:
        self.__direction = True  # CW
      else:
        self.__direction = False  # CCW

    self.__prev_encoderA_val = encoderA_val
    self.__prev_encoderB_val = encoderB_val

  def getEncoderDirection(self):
    with self.__IRS_LOCK:
      return self.__direction  # True for CW, False for CCW

  def getEncoderSpeed(self):
    with self.__IRS_LOCK:
      return self.__encoderSpeed

  def stop(self):
    self.encoderRunning = False
    if self.__interrupt_thread.is_alive():
      self.__interrupt_thread.join()

  def __del__(self):
    self.stop()