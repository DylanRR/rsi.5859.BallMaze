from gpiozero import DigitalOutputDevice
from time import sleep


class rsiStepMotor:
  def __init__(self, stepPin, dirPin, enablePin):
    self.__power = 0
    self.__currentPosition = 0
    self.__homePosition = 0
    self.__endPosition = None
    self.__trackSteps = None
    self.__direction = None    # True = Clockwise, False = Counter Clockwise

    self.__mStep = DigitalOutputDevice(stepPin, active_high=True, initial_value=False)
    self.__mDir = DigitalOutputDevice(dirPin, active_high=True, initial_value=False)
    self.__mEnable = DigitalOutputDevice(enablePin, active_high=True, initial_value=False)

    self.__stepIncrement = 1
    self.__stepDelay = 0.01
    self.__rampingPower = None
    self.__currentRampPower = 0
    self.__internalMaxDelay = 0.00009
    self.__internalMinDelay = 0.009
    self.__motorMoving = False
    self.__exitMove = False
  
  def __del__(self):
    self.close()

  def close(self):
    #self.disableMotor()
    self.__mStep.close()
    self.__mDir.close()
    self.__mEnable.close()
    
  def calibrateTrack(self, homePosition, endPosition):
    self.__homePosition = homePosition
    self.__endPosition = endPosition
    self.__trackSteps = endPosition - homePosition

  def overWriteCurrentPosition(self, position):
    self.__currentPosition = position

  def getStepIncrement(self):
    return self.__stepIncrement

  def getHomePosition(self):
    return self.__homePosition
  
  def getEndPosition(self):
    return self.__endPosition

  def getTrackSteps(self):
    return self.__trackSteps

  def getCurrentPosition(self):
    return self.__currentPosition
  
  def enableMotor(self):
    self.__mEnable.value = False
  
  def disableMotor(self):
    self.__mEnable.value = True

  def haltMotor(self, message="Internal Halt"):
    self.disableMotor()
    print(f"Motor Halted: {message}")
  
  def resetRamping(self):
    self.__rampingPower = False
    self.__currentRampPower = 0
    self.setPower(self.__power)

  def getDirection(self):
    return self.__direction

  def setDirection(self, clockwise): #True=Right (Clockwise), False=Left (Counter Clockwise)
    if self.__direction != clockwise:
      self.resetRamping()
      self.__mDir.value = clockwise
      self.__direction = clockwise

  def __calcDelay(self, power):
    # Map the constrained power to the delay range
    # Formula: mapped_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    self.__stepDelay = ((power - 1) * (self.__internalMaxDelay - self.__internalMinDelay) / (100 - 1)) + self.__internalMinDelay

  def setPower(self, power, rampPower=True):
    # Constrain power to be between 1 and 100
    constrained_power = max(0, min(power, 100))

    # Check if there is a change in power; if not, return
    if constrained_power == self.__power:
      return

    # Check for power of 0
    if constrained_power == 0:
      self.__power = 0
      self.__checkForExit()
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
  
  def __updatePower(self):
    if not self.__rampingPower:
        return
    difference = self.__power - self.__currentRampPower
    adjustment = difference * 0.01  # 5% of the difference

    # Update the current ramp power without overshooting
    if abs(adjustment) < 0.01:
        self.__currentRampPower = self.__power
    else:
        self.__currentRampPower += adjustment

    # Check if the target power is reached or exceeded
    if (adjustment > 0 and self.__currentRampPower >= self.__power) or \
        (adjustment < 0 and self.__currentRampPower <= self.__power):
        self.__currentRampPower = self.__power
        self.__rampingPower = False

    self.__calcDelay(self.__currentRampPower)

  def __checkForExit(self):
    if self.__power == 0:
      self.__exitMove = True
      self.resetRamping()

  def isMotorMoving(self):
    return self.__motorMoving
      

  def moveMotor(self, steps, clockwise, power=50, trackPos=True, overRideRamp=False):
    self.setDirection(clockwise)
    self.setPower(power, not overRideRamp)
    self.__motorMoving = True
    self.__exitMove = False
    #print(f"Moving Motor {steps} steps in {'Clockwise' if clockwise else 'Counter Clockwise'} power: {power} stepDelay: {self.__stepDelay}")
    for i in range(steps):
      if self.__exitMove:
        break
      self.__mStep.on()
      sleep(self.__stepDelay)
      self.__mStep.off()
      sleep(self.__stepDelay)
      if trackPos:
        self.__currentPosition += -1 if clockwise else 1
      self.__updatePower()
      self.__checkForExit()
    self.__exitMove = False
    self.__motorMoving = False

  