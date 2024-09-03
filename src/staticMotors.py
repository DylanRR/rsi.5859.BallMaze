from rsiStepMotor import rsiStepMotor

MOTOR_1_ENABLE = 21             #Pin Label: 21      Wire Color:White    #Left Motor
MOTOR_1_DIRECTION = 22          #Pin Label: 22      Wire Color:Green    #Left Motor
MOTOR_1_STEP = 23               #Pin Label: 23      Wire Color:Brown    #Left Motor

MOTOR_2_ENABLE = 18             #Pin Label: 18      Wire Color:White    #Horizontal Motor
MOTOR_2_DIRECTION = 19          #Pin Label: 19      Wire Color:Green    #Horizontal Motor
MOTOR_2_STEP = 20               #Pin Label: 20      Wire Color:Brown    #Horizontal Motor

MOTOR_3_ENABLE = 24             #Pin Label: 24      Wire Color:White    #Right Motor
MOTOR_3_DIRECTION = 25          #Pin Label: 25      Wire Color:Green    #Right Motor
MOTOR_3_STEP = 26               #Pin Label: 26      Wire Color:Brown    #Right Motor


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