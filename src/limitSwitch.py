from gpiozero import Button
from rsiStepMotor import rsiStepMotor
import inspect
from typing import List
import sys

class haltingLimitSwitch:
  def __init__(self, pin: int, motorObjs: List[rsiStepMotor], pullUp: bool = True, bounceTime: float = 0.02):
    self.pin = pin
    self.objName = self.__getObjName()
    self.switch = Button(pin, pull_up=pullUp, bounce_time=bounceTime)
    self.switch.when_deactivated = self.__haultMotor
    self.motors = motorObjs

  def __getObjName(self) -> str:
    frame = inspect.currentframe().f_back
    for name, obj in frame.f_locals.items():
      if obj is self:
        return name
    return None

  def __del__(self):
    self.switch.close()

  def close(self):
    self.__del__()

  def __haultMotor(self):
    for index, motor in enumerate(self.motors, start=1):
      hMsg = f"{self.objName} Activated: Halting Motor - {index}" # Debug message
      motor.haltMotor(hMsg, False)
    sys.exit(1)


class limitSwitch:
  def __init__(self, pin: int, pullUp: bool = True, bounceTime: float = 0.02):
    self.pin = pin
    self.objName = self.__getObjName()
    self.switch = Button(pin, pull_up=pullUp, bounce_time=bounceTime)
    self.switch.when_deactivated = self.__isr
    self.__lockedOut = False
    self.__firstCalibration = False
    self.__secondCalibration = False

  def __del__(self):
    self.switch.close()
  def close(self):
    self.__del__()

  def __getObjName(self) -> str:
    frame = inspect.currentframe().f_back
    for name, obj in frame.f_locals.items():
      if obj is self:
        return name
    return None

  def nonCalISR(self):
    print("Non-calibration ISR Event")

  def __isr(self):
    print(f"Entering ISR for Pin {self.pin}")
    if self.__lockedOut:
      return
    print("ISR not locked out...")
    if not self.__firstCalibration:
      print("Entering First Calibration...")
      self.__firstCalibration = True
      self.__lockedOut = True
      return
    if not self.__secondCalibration:
      print("Entering Second Calibration...")
      self.__secondCalibration = True
      self.__lockedOut = True
      return
    self.nonCalISR()

  def getFirstCalibration(self) -> bool:
    return self.__firstCalibration

  def getSecondCalibration(self) -> bool:
    return self.__secondCalibration

  def setLockedOut(self, lock: bool):
    self.__lockedOut = lock
