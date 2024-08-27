from time import sleep
from gpiozero import Button
from rsiStepMotor import rsiStepMotor

#GPIO PI Pins
BTN_ESTOP = 0                   #Pin Label: EED     Wire Color: Red
SDA_BUS = 2                     #Pin Label: SDA     Wire Color: Orange
SCL_BUS = 3                     #Pin Label: SCL     Wire Color: Purple
LS_TOP_RIGHT = 4                #Pin Label: 4       Wire Color: Red
LS_BOTTOM_RIGHT = 5             #Pin Label: 5       Wire Color:Red
LS_CALIBRATE_RIGHT = 6          #Pin Label: 6       Wire Color:Red
LS_TOP_LEFT = 7                 #Pin Label: CE1     Wire Color:Red
LS_BOTTOM_LEFT = 8              #Pin Label: CE0     Wire Color:Red
LS_CALIBRATE_LEFT = 9           #Pin Label: MISO    Wire Color:Red
LS_HORIZONTAL_RIGHT_STOP = 10   #Pin Label: MOSI    Wire Color:White
LS_HORIZONTAL_RIGHT_INIT = 11   #Pin Label: SCLK    Wire Color:Red
LS_HORIZONTAL_LEFT_STOP = 12    #Pin Label: 12      Wire Color:White
LS_HORIZONTAL_LEFT_INIT = 13    #Pin Label: 13      Wire Color:Red
ENCODER_1_A = 14                #Pin Label: TXD     Wire Color:Brown
ENCODER_1_B = 15                #Pin Label: RXD     Wire Color:White
ENCODER_2_A = 16                #Pin Label: 16      Wire Color:Brown
ENCODER_2_B = 17                #Pin Label: 17      Wire Color:White
MOTOR_2_ENABLE = 18             #Pin Label: 18      Wire Color:White
MOTOR_2_DIRECTION = 19          #Pin Label: 19      Wire Color:Green
MOTOR_2_STEP = 20               #Pin Label: 20      Wire Color:Brown
MOTOR_1_ENABLE = 21             #Pin Label: 21      Wire Color:White
MOTOR_1_DIRECTION = 22          #Pin Label: 22      Wire Color:Green
MOTOR_1_STEP = 23               #Pin Label: 23      Wire Color:Brown
MOTOR_3_ENABLE = 24             #Pin Label: 24      Wire Color:White
MOTOR_3_DIRECTION = 25          #Pin Label: 25      Wire Color:Green
MOTOR_3_STEP = 26               #Pin Label: 26      Wire Color:Brown

motor1 = rsiStepMotor(MOTOR_1_STEP, MOTOR_1_DIRECTION, MOTOR_1_ENABLE)
motor2 = rsiStepMotor(MOTOR_2_STEP, MOTOR_2_DIRECTION, MOTOR_2_ENABLE)
motor3 = rsiStepMotor(MOTOR_3_STEP, MOTOR_3_DIRECTION, MOTOR_3_ENABLE)

btn_estop = Button(BTN_ESTOP, pull_up=True, bounce_time=0.2)
TR_ls_halt = Button(LS_TOP_RIGHT, pull_up=True)
BR_ls_halt = Button(LS_BOTTOM_RIGHT, pull_up=True)
TL_ls_halt = Button(LS_TOP_LEFT, pull_up=True)
BL_ls_halt = Button(LS_BOTTOM_LEFT, pull_up=True)
#HR_ls_halt = Button(LS_HORIZONTAL_RIGHT_STOP, pull_up=True)
#HL_ls_halt = Button(LS_HORIZONTAL_LEFT_STOP, pull_up=True)

def motorHault(message):
  motor1.haltMotor(message, True)
  motor2.haltMotor(message, True)
  motor3.haltMotor(message, True)

btn_estop.when_deactivated = lambda: motorHault("Estop Button Pressed")
TR_ls_halt.when_deactivated = lambda: motorHault("Top Right Limit Switch Pressed")
TL_ls_halt.when_deactivated = lambda: motorHault("Top Left Limit Switch Pressed")
BR_ls_halt.when_deactivated = lambda: motorHault("Bottom Right Limit Switch Pressed")
BL_ls_halt.when_deactivated = lambda: motorHault("Bottom Left Limit Switch Pressed")
#HR_ls_halt.when_deactivated = lambda: motorHault("Horizontal Right Halt Limit Switch Pressed")
#HL_ls_halt.when_deactivated = lambda: motorHault("Horizontal Left Halt Limit Switch Pressed")

def testEnable():
  motor1.enableMotor()
  print("Motor 1 Enabled")
  sleep(3)
  motor1.disableMotor()
  print("Motor 1 Disabled")
  sleep(3)
  motor3.enableMotor()
  print("Motor 3 Enabled")
  sleep(3)
  motor3.disableMotor()
  print("Motor 3 Disabled")

def moveDirection():
  motor1.enableMotor()
  print("Motor 1 Enabled")
  sleep(.5)
  motor1.moveMotor(20, True, 30, False)
  print("Motor 1 Moved 20 steps clockwise")
  sleep(3)
  motor1.moveMotor(20, False, 30, False)
  print("Motor 1 Moved 20 steps counter clockwise")
  sleep(3)
  motor1.disableMotor()
  sleep(.5)
  motor3.enableMotor()
  print("Motor 3 Enabled")
  sleep(.5)
  motor3.moveMotor(20, True, 30, False)
  print("Motor 3 Moved 20 steps clockwise")
  sleep(3)
  motor3.moveMotor(20, False, 30, False)
  print("Motor 3 Moved 20 steps counter clockwise")
  sleep(3)
  motor3.disableMotor()
  

def enable_disable_all():
  motor1.enableMotor()
  motor2.enableMotor()
  motor3.enableMotor()
  input("Press Enter to exit...")
  motor1.disableMotor()
  motor2.disableMotor()
  motor3.disableMotor()

def moveVirtual(step, direction, speed):
  motor1.enableMotor()
  motor3.enableMotor()
  for i in range(0, step):
    motor1.moveMotor(1, direction, speed, False)
    #motor2.moveMotor(1, direction, speed, False)
    motor3.moveMotor(1, direction, speed, False)
  motor1.disableMotor()
  motor3.disableMotor()


def main():
  moveVirtual(6000, False, 98)
  #motor2.enableMotor()
  #motor2.moveMotor(4000, True, 95, False)
  #motor2.disableMotor()

  #motor1.enableMotor()
  #motor1.moveMotor(20, True, 10, False)
  #motor1.disableMotor()





if __name__ == "__main__":
    main()
