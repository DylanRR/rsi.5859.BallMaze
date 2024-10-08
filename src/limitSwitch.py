from gpiozero import Button
import inspect
import staticMotors as sMotor

class mHaltException(Exception):
  def __init__(self, message):
    super().__init__(message)

class haltingLimitSwitch:
  def __init__(self, name: str, pin: int, pullUp: bool = True, bounceTime: float = 0.02):
    self.pin = pin
    self.objName = name
    self.switch = Button(pin, pull_up=pullUp, bounce_time=bounceTime)
    self.switch.when_deactivated = self.__haltMotor

  def __del__(self):
    self.close()
  def close(self):
    self.switch.close()

  def __haltMotor(self):
    sMotor.disableAllMotors(self.objName)

  def triggerHaltEvent(self):
    self.__haltMotor()


class limitSwitch:
  def __init__(self, pin: int, pullUp: bool = True, bounceTime: float = 0.01):
    self.pin = pin
    self.objName = self.__getObjName()
    self.switch = Button(pin, pull_up=pullUp, bounce_time=bounceTime)
    self.switch.when_deactivated = self.__isr
    self.__lockedOut = False
    self.__firstCalibration = False
    self.__secondCalibration = False

  def __del__(self):
    self.close()
  def close(self):
    self.switch.close()

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
