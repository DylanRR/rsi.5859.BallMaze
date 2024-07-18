from gpiozero import OutputDevice
from time import sleep
import os

class rsiStepMotor:
  def __init__(self, stepPin, dirPin, enablePin):
    self.stepPin = stepPin
    self.dirPin = dirPin
    self.enablePin = enablePin
    self.__power = 1
    self.currentPosition = 0
    self.homePosition = 0
    self.endPosition = 0
    self.steps = 0
    self.direction = True    # True = Clockwise, False = Counter Clockwise
    self.__mStep = OutputDevice(self.stepPin)
    self.__mDir = OutputDevice(self.dirPin)
    self.__mEnable = OutputDevice(self.enablePin)
    self.__stepDelay = 0.01
    self.__rampingPower = False
    self.__currentRampPower = 0
    self.__internalMaxDelay = 0.1
    self.__internalMinDelay = 0.00001

  def enableMotor(self):
    self.__mEnable.off()
  
  def disableMotor(self):
    self.__mEnable.on()

  def haltMotor(self, message="Internal Halt", hardExit=True):
    self.disableMotor()
    print(f"Motor Halted: {message}")
    if hardExit:
      os._exit(1)

  def resetRamping(self):
    self.__rampingPower = False
    self.__currentRampPower = 0
    self.setPower(self.__power)

  def setDirection(self, clockwise): #True=Right (Clockwise), False=Left (Counter Clockwise)
    if self.direction != clockwise:
      self.resetRamping()
      self.__mDir.value = clockwise

  def __calcDelay(self, power):
    # Map the constrained power to the delay range
    # Formula: mapped_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    self.__stepDelay = ((power - 1) * (self.__internalMaxDelay - self.__internalMinDelay) / (100 - 1)) + self.__internalMinDelay

  def setPower(self, power, rampPower=True):
    # Constrain power to be between 1 and 100
    constrained_power = max(1, min(power, 100))

    # Check if there is a change in power; if not, return
    if constrained_power == self.__power:
      return

    # Check if rampPower is True
    if not rampPower:
      self.__power = constrained_power
      self.__calcDelay(constrained_power)
      return
    
    # Check if we are currently ramping
    if self.__rampingPower:
      # Check if the passed in power is above or below currentRampPower by 10%
      if abs(constrained_power - self.__currentRampPower) > self.__currentRampPower * 0.1:
        self.__rampingPower = True
        self.__power = constrained_power
      else:
        self.__rampingPower = False
        self.__power = constrained_power
        self.__calcDelay(constrained_power)
      return

    # If not ramping, check if the passed in power is 10% over or under current power
    if abs(constrained_power - self.__power) > self.__power * 0.1:
      self.__rampingPower = True
      self.__currentRampPower = self.__power
      self.__power = constrained_power
    else:
      self.__rampingPower = False
      self.__power = constrained_power
      self.__calcDelay(constrained_power)
  
  def __updatePower(self): #Update
    if not self.__rampingPower:
      return
    if self.__currentRampPower == self.__power:
      self.__rampingPower = False
      return
    if self.__currentRampPower > self.__power:
      self.__currentRampPower -= .01
    else:
      self.__currentRampPower += .01
    self.__calcDelay(self.__currentRampPower)

  def moveMotor(self, steps, clockwise, power=50, trackPos=True):
    self.setDirection(clockwise)
    self.setPower(power)
    for i in range(steps):
      self.__mStep.on()
      sleep(self.__stepDelay)
      self.__mStep.off()
      sleep(self.__stepDelay)
      if trackPos:
        self.currentPosition += 1 if clockwise else -1
      self.__updatePower()
  