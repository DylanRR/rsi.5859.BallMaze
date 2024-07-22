from gpiozero import Button
from rsiEncoder import rsiEncoder
from typing import List

class limitSwitch:
  def __init__(self, pin: int, encoderObjs: List[rsiEncoder], pullUp: bool = True):
    self.pin = pin
    self.encoders = encoderObjs  # Store the list of encoder objects
    self.__switch = Button(pin, pull_up=pullUp)
    self.__lockedOut = False
    self.__firstCalibration = False
    self.__secondCalibration = False
    self.__switch.when_pressed = self.__irs

  def __del__(self):
    pass  # Cleanup GPIO

  def __lockOutEncoders(self, lock: bool):
    for encoder in self.encoders:
      encoder.setIRSLock(lock)

  def nonCalISR(self):
    pass  # Placeholder for the non-calibration ISR

  def __irs(self):
    if self.__lockedOut:
      return
    self.__lockOutEncoders(True)

    if not self.__firstCalibration:
      self.__firstCalibration = True
      self.__lockedOut = True
      return

    if not self.__secondCalibration:
      self.__secondCalibration = True
      self.__lockedOut = True
      return

    self.nonCalISR()
    self.__lockOutEncoders(False)

  def getFirstCalibration(self) -> bool:
    return self.__firstCalibration

  def getSecondCalibration(self) -> bool:
    return self.__secondCalibration

  def setLockedOut(self, lock: bool):
    self.__lockedOut = lock