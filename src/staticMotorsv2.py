from rsiStepMotorv2 import rsiDuelStepMotor

MOTOR_1_ENABLE = 5             #Pin Label: TXD     Wire Color:White
MOTOR_1_DIRECTION = 12          #Pin Label: RXD     Wire Color:Green
MOTOR_1_STEP = 6               #Pin Label: 18      Wire Color:Brown
MOTOR_2_ENABLE = 13             #Pin Label: 23      Wire Color:White
MOTOR_2_DIRECTION = 16          #Pin Label: 24      Wire Color:Green
MOTOR_2_STEP = 19               #Pin Label: 25      Wire Color:Brown
MOTOR_3_ENABLE = 20              #Pin Label: CE0     Wire Color:White
MOTOR_3_DIRECTION = 26           #Pin Label: CE1     Wire Color:Green
MOTOR_3_STEP = 21                #Pin Label: EEC     Wire Color:Brown


# Initialize Motor
verticalMotors = rsiDuelStepMotor()
verticalMotors.initMotor1(MOTOR_1_STEP, MOTOR_1_DIRECTION, MOTOR_1_ENABLE)
verticalMotors.initMotor2(MOTOR_3_STEP, MOTOR_3_DIRECTION, MOTOR_3_ENABLE)

horizontalMotors = rsiDuelStepMotor()
horizontalMotors.initMotor1(MOTOR_2_STEP, MOTOR_2_DIRECTION, MOTOR_2_ENABLE)

motors = [verticalMotors, horizontalMotors]
motors_halted = False
halt_reason = ""

#Disable all motors
def disableAllMotors(haltReason="Null"):
  global motors_halted
  for motor in motors:
    motor.disableMotors()
  motors_halted = True
  halt_reason = haltReason

#Object cleanup
def cleanup():
  for motor in motors:
    motor.close()

