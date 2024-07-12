v=0.2
#v0.1 - Setup encoder and limit switches
#v0.2 - add Gantry Stepper Motor

import board
import busio
from digitalio import Direction
from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)
mcp = MCP23017(i2c, address=0x20)
import digitalio
import datetime
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

def EStopCheck_Button(ch):
    print("Emergency Stop Pressed")
    print("System Stopped")
    EStopCheck_End()

def EStopCheck_LimitA2(ch):
    print("Outer Limit Stop")
    print("Outer Limit Switch #1")
    print("System Stopped")
    EStopCheck_End()

def EStopCheck_LimitB2(ch):
    print("Outer Limit Stop")
    print("Outer Limit Switch #2")
    print("System Stopped")
    EStopCheck_End()

def EStopCheck_End(ch):
    gantryMotor.motor_stop()
    GPIO.output(gantryEn,GPIO.LOW)
    while(1):
        pass
    
def encoderInterrupt():
    global encoderA
    global encoderB
    global PinANew
    global PinBNew
    global PinAOld
    global PinBOld
    global EncoderCount
    global enDir
    global TimeOld
    global TimeNew
    global TimeVerify
    global timedelta
    
    PinANew = encoderA.value
    PinBNew = encoderB.value

    if PinANew == PinAOld and PinBNew == PinBOld:
        if TimeVerify == 0:
            timedelta = datetime.datetime.now() - TimeOld
            timedelta = timedelta.total_seconds()
            if timedelta >= 0.25:
                TimeVerify = 1
                EncoderCount = 0
        return
    
    TimeNew = datetime.datetime.now()
    
    if PinANew != PinBOld:
      enDir = enDir + 1
    else:
      enDir = enDir - 1
      
    PinAOld = PinANew;
    PinBOld = PinBNew;
    
    if enDir >= enDirChange:
        enDir = enDirChange
        EncoderCount = EncoderCount + 1
    elif enDir <= (enDirChange *-1):
        enDir = enDirChange * -1
        EncoderCount = EncoderCount -1

    if EncoderCount < 0:
      EncoderCount = 0
    elif EncoderCount > MaxPos:
      EncoderCount = MaxPos
    
    TimeVerify = 0
    timedelta = TimeNew - TimeOld
    timedelta = timedelta.total_seconds() * 1000
    #print(timedelta)
    TimeOld = TimeNew
    
    #Report Output
    #print(str(enDir) + "-" + str(EncoderCount))

def Homing():
    print("Homing...")
    GPIO.output(gantryEn,GPIO.HIGH) # pull enable to low to enable motor
    #gantryMotor.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                        #"Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                        #2000, # number of steps
                        #.005, # step delay [sec]
                        #False, # True = print verbose output 
                        #.1) # initial delay [sec]
    #GPIO.output(gantryEn,GPIO.LOW)
    print("Done")

#Setup
#Setup MCP23017
global encoderA
encoderA = mcp.get_pin(8)
encoderA.direction = digitalio.Direction.INPUT
encoderA.pull = digitalio.Pull.UP
global encoderB
encoderB = mcp.get_pin(9)
encoderB.direction = digitalio.Direction.INPUT
encoderB.pull = digitalio.Pull.UP
global encoderZ
encoderZ = mcp.get_pin(10)
encoderZ.direction = digitalio.Direction.INPUT
encoderZ.pull = digitalio.Pull.UP

#Limit Switches
global LimitA1
GPIO.setmode(GPIO.BCM)
LimitA1 = 10
GPIO.setup(LimitA1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
global LimitA2
LimitA2 = 9
GPIO.setup(LimitA2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
global LimitB1
LimitB1 = 11
GPIO.setup(LimitB1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
global LimitB2
LimitB2 = 12
GPIO.setup(LimitB2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
global EmergencyStop
EmergencyStop = 4
GPIO.setup(EmergencyStop, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(EmergencyStop, GPIO.RISING, callback=EStopCheck_Button)
#GPIO.add_event_detect(LimitA2, GPIO.RISING, callback=EStopCheck_LimitA2)
#GPIO.add_event_detect(LimitB2, GPIO.RISING, callback=EStopCheck_LimitB2)

#Encoder Variables
global PinANew
PinANew=0
global PinAOld
PinAOld=0
global PinBNew
PinBNew=0
global PinBOld
PinBOld=0
global EncoderCount
EncoderCount = 0
global enDir
enDir = 0
global MaxPos
MaxPos=500
global enDirChange
enDirChange = 2

#Time Calc Setup
global TimeOld
TimeOld = datetime.datetime.now()
global TimeNew
TimeNew = TimeOld - datetime.timedelta(seconds = 10)
global TimeVerify
global timedelta
TimeVerify = 0

#Stepper Motor Setup
global gantryDir
gantryDir = 27
GPIO.setup(gantryDir, GPIO.OUT)
global gantryStep
gantryStep = 22
GPIO.setup(gantryStep, GPIO.OUT)
global gantryEn
gantryEn = 17
GPIO.setup(gantryEn, GPIO.OUT)

gantryMotor = RpiMotorLib.A4988Nema(gantryDir, gantryStep, (21,21,21), "DRV8825")
GPIO.setup(gantryEn,GPIO.OUT) # set enable pin as output

#Setup MCP23017 Interupt
#mcp.interrupt_enable = 0xFFFF
#mcp.interrupt_configuration = 0x0000  # interrupt on any change
#mcp.io_control = 0x44  # Interrupt as open drain and mirrored
#mcp.clear_ints()  # Interrupts need to be cleared initially

print("Ball Maze v",v," Starting...")

Homing()

while(1):
    encoderInterrupt()
    print(GPIO.input(LimitA1))
