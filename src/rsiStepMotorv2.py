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
    
    self.__threadLock = threading.Lock()

    self.__


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

  def setDirection(self, direction):
    self.__m1Dir.value = direction
    self.__m2Dir.value = direction

  def enableMotors(self):
    self.__m1Enable.off()
    self.__m2Enable.off()

  def disableMotors(self):
    self.__m1Enable.on()
    self.__m2Enable.on()

  def setTargetSpeed(self, speed):
    # Acquire the lock to safely update __targetSpeed
    with self.__threadLock:
      self.__targetSpeed = speed

  def __updatePulseRate(self):
    # Acquire the lock to safely read __targetSpeed
    with self.__threadLock:
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

  def pulseFactory(self, condition, direction, motor1=True, motor2=True):
    """Factory method to pulse motors based on the given condition."""
    self.enableMotors()
    self.setDirection(direction)
    self.setTargetSpeed(0)
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

    while condition():
      pulse()
      self.__updatePulseRate()

    self.__targetSpeed = None
    self.__pulseRate = None
    self.disableMotors()


