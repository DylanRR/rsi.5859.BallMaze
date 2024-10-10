from deprecated.rsiStepMotor import rsiStepMotor

MOTOR_1_ENABLE = 14             #Pin Label: TXD     Wire Color:White
MOTOR_1_DIRECTION = 15          #Pin Label: RXD     Wire Color:Green
MOTOR_1_STEP = 18               #Pin Label: 18      Wire Color:Brown
MOTOR_2_ENABLE = 23             #Pin Label: 23      Wire Color:White
MOTOR_2_DIRECTION = 24          #Pin Label: 24      Wire Color:Green
MOTOR_2_STEP = 25               #Pin Label: 25      Wire Color:Brown
MOTOR_3_ENABLE = 8              #Pin Label: CE0     Wire Color:White
MOTOR_3_DIRECTION = 7           #Pin Label: CE1     Wire Color:Green
MOTOR_3_STEP = 1                #Pin Label: EEC     Wire Color:Brown


# Initialize Motor
motor1 = rsiStepMotor(MOTOR_1_STEP, MOTOR_1_DIRECTION, MOTOR_1_ENABLE)
motor2 = rsiStepMotor(MOTOR_2_STEP, MOTOR_2_DIRECTION, MOTOR_2_ENABLE)
motor3 = rsiStepMotor(MOTOR_3_STEP, MOTOR_3_DIRECTION, MOTOR_3_ENABLE)
motors = [motor1, motor2, motor3]

motors_halted = False
halt_reason = ""


#Disable all motors
def disableAllMotors(haltReason="Null"):
  global motors_halted, halt_reason
  motor3.haltMotor("Motor 3")
  motor1.haltMotor("Motor 1")
  motor2.haltMotor("Motor 2")

  motors_halted = True
  halt_reason = haltReason

#Object cleanup
def cleanup():
  for motor in motors:
    motor.close()