from gpiozero import DigitalOutputDevice
from time import sleep
import threading

class rsiDuelStepMotor:
  def __init__(self):
    self.__m1Step = None
    self.__m1Dir = None
    self.__m1Enable = None
    self.__m2Step = None
    self.__m2Dir = None
    self.__m2Enable = None
    self.__pins = set()

    self.__targetSpeed = None
    self.__pulseRate = None
    self.__constPulseMin = 0.0008
    self.__constPulseMax = 0.01
    self.__constPulseDelta = (self.__constPulseMax - self.__constPulseMin) / 100
    
    self.__speedLock = threading.Lock()
    self.__positionLock = threading.Lock()

    self.__direction = None
    self.__position = 0
    self.__endPosition = None


  def initMotor1(self, stepPin, dirPin, enablePin):
    self.__m1Step = DigitalOutputDevice(stepPin, active_high=True, initial_value=False)
    self.__m1Dir = DigitalOutputDevice(dirPin, active_high=True, initial_value=False)
    self.__m1Enable = DigitalOutputDevice(enablePin, active_high=True, initial_value=False)
    self.__pins.update({self.__m1Step, self.__m1Dir, self.__m1Enable})

  def initMotor2(self, stepPin, dirPin, enablePin):
    self.__m2Step = DigitalOutputDevice(stepPin, active_high=True, initial_value=False)
    self.__m2Dir = DigitalOutputDevice(dirPin, active_high=True, initial_value=False)
    self.__m2Enable = DigitalOutputDevice(enablePin, active_high=True, initial_value=False)
    self.__pins.update({self.__m2Step, self.__m2Dir, self.__m2Enable})



  def __del__(self):
    self.close()

  def close(self):
    for pin in self.__pins:
      if pin is not None:
        pin.close()

  def __setDirection(self, direction):
    if self.__m1Dir is not None:
      self.__m1Dir.value = direction
    if self.__m2Dir is not None:
      self.__m2Dir.value = direction

  def enableMotors(self):
    if self.__m1Enable is not None:
      self.__m1Enable.off()
    if self.__m2Enable is not None:
      self.__m2Enable.off()

  def disableMotors(self):
    if self.__m1Enable is not None:
      self.__m1Enable.on()
    if self.__m2Enable is not None:
      self.__m2Enable.on()

  def overwritePosition(self, position):
    with self.__positionLock:
      self.__position = position

  def getPosition(self):
    with self.__positionLock:
      return self.__position

  def setEndPosition(self, position):
    self.__endPosition = position
  def getEndPosition(self):
    return self.__endPosition

  def setTargetSpeed(self, speed):
    # Acquire the lock to safely update __targetSpeed
    with self.__speedLock:
      self.__targetSpeed = speed

  def __updatePulseRate(self):
    # Acquire the lock to safely read __targetSpeed
    with self.__speedLock:
       targetSpeed = self.__targetSpeed
    
    pRate = self.__pulseRate
    maxPulse = self.__constPulseMax
    if pRate is None:
        pRate = maxPulse

    delta = self.__constPulseDelta
    minPulse = self.__constPulseMin

    inverted_value = 100 - targetSpeed
    mappedTarget = minPulse + (inverted_value / 100) * (maxPulse - minPulse)

    if mappedTarget > pRate:
        pRate = min(pRate + delta, maxPulse)
    elif mappedTarget < pRate:
        pRate = max(pRate - delta, minPulse)

    self.__pulseRate = pRate

  def __doubleMotorPulse(self):
    self.__m1Step.on()
    self.__m2Step.on()
    sleep(self.__pulseRate)
    self.__m1Step.off()
    self.__m2Step.off()
    sleep(self.__pulseRate)

  def __motor1Pulse(self):
    self.__m1Step.on()
    sleep(self.__pulseRate)
    self.__m1Step.off()
    sleep(self.__pulseRate)

  def __motor2Pulse(self):
    self.__m2Step.on()
    sleep(self.__pulseRate)
    self.__m2Step.off()
    sleep(self.__pulseRate)

  def pulseFactory(self, direction, condition=None, iterations=None, motor1=True, motor2=True, initialTargetSpeed=0):
    """Factory method to pulse motors based on the given condition."""
    self.enableMotors()
    self.__setDirection(direction)
    self.setTargetSpeed(initialTargetSpeed)
    self.__updatePulseRate()
    if motor1 and motor2:
      pulse = self.__doubleMotorPulse
    elif motor1:
      pulse = self.__motor1Pulse
    elif motor2:
      pulse = self.__motor2Pulse
    else:
      self.disableMotors()
      return  # No motors to pulse
    
    if iterations is not None:
      for _ in range(iterations):
        pulse()
        self.__updatePulseRate()
        with self.__positionLock:
          self.__position += 1 if direction else -1
    elif condition is not None:
      while condition():
        pulse()
        self.__updatePulseRate()
        with self.__positionLock:
          self.__position += 1 if direction else -1

    self.__targetSpeed = None
    self.__pulseRate = None
    self.disableMotors()


