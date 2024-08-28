from gpiozero import Button
from encoderv2 import Encoder
from rsiStepMotor import rsiStepMotor
from limitSwitch import haltingLimitSwitch, limitSwitch
import os

#GPIO PI Pins
SDA_BUS = 2                     #Pin Label: SDA     Wire Color: Orange
SCL_BUS = 3                     #Pin Label: SCL     Wire Color: Purple

BTN_ESTOP = 0                   #Pin Label: EED     Wire Color: Red
LS_TOP_RIGHT = 4                #Pin Label: 4       Wire Color: Red
LS_BOTTOM_RIGHT = 5             #Pin Label: 5       Wire Color:Red
LS_CALIBRATE_RIGHT = 6          #Pin Label: 6       Wire Color:Red
LS_TOP_LEFT = 7                 #Pin Label: CE1     Wire Color:Red
LS_BOTTOM_LEFT = 8              #Pin Label: CE0     Wire Color:Red
LS_CALIBRATE_LEFT = 9           #Pin Label: MISO    Wire Color:Red
LS_HORIZONTAL_RIGHT_INIT = 10   #Pin Label: MOSI    Wire Color:Red
LS_HORIZONTAL_RIGHT_STOP = 11   #Pin Label: SCLK    Wire Color:White
LS_HORIZONTAL_LEFT_INIT = 12    #Pin Label: 12      Wire Color:Red
LS_HORIZONTAL_LEFT_STOP = 13    #Pin Label: 13      Wire Color:White



ENCODER_1_A = 14                #Pin Label: TXD     Wire Color:Brown
ENCODER_1_B = 15                #Pin Label: RXD     Wire Color:White

ENCODER_2_A = 16                #Pin Label: 16      Wire Color:Brown
ENCODER_2_B = 17                #Pin Label: 17      Wire Color:White


MOTOR_1_ENABLE = 21             #Pin Label: 21      Wire Color:White    #Left Motor
MOTOR_1_DIRECTION = 22          #Pin Label: 22      Wire Color:Green    #Left Motor
MOTOR_1_STEP = 23               #Pin Label: 23      Wire Color:Brown    #Left Motor

MOTOR_2_ENABLE = 18             #Pin Label: 18      Wire Color:White    #Horizontal Motor
MOTOR_2_DIRECTION = 19          #Pin Label: 19      Wire Color:Green    #Horizontal Motor
MOTOR_2_STEP = 20               #Pin Label: 20      Wire Color:Brown    #Horizontal Motor

MOTOR_3_ENABLE = 24             #Pin Label: 24      Wire Color:White    #Right Motor
MOTOR_3_DIRECTION = 25          #Pin Label: 25      Wire Color:Green    #Right Motor
MOTOR_3_STEP = 26               #Pin Label: 26      Wire Color:Brown    #Right Motor




# Initialize Encoders
encoder1 = Encoder(ENCODER_1_A, ENCODER_1_B)
encoder2 = Encoder(ENCODER_2_A, ENCODER_2_B)

# Initialize Motor
motor1 = rsiStepMotor(MOTOR_1_STEP, MOTOR_1_DIRECTION, MOTOR_1_ENABLE)
motor2 = rsiStepMotor(MOTOR_2_STEP, MOTOR_2_DIRECTION, MOTOR_2_ENABLE)
motor3 = rsiStepMotor(MOTOR_3_STEP, MOTOR_3_DIRECTION, MOTOR_3_ENABLE)
motors = [motor1, motor2, motor3]

# Initialize Haulting Limit Switches
btn_estop = haltingLimitSwitch("btn_estop", BTN_ESTOP, motors)
TR_ls_halt = haltingLimitSwitch("TR_ls_halt", LS_TOP_RIGHT, motors)
BR_ls_halt = haltingLimitSwitch("BR_ls_halt", LS_BOTTOM_RIGHT, motors)
TL_ls_halt = haltingLimitSwitch("TL_ls_halt", LS_TOP_LEFT, motors, False)  #NOTE: May need to turn of the pullup resistor
BL_ls_halt = haltingLimitSwitch("BL_ls_halt", LS_BOTTOM_LEFT, motors)
HR_ls_halt = haltingLimitSwitch("HR_ls_halt", LS_HORIZONTAL_RIGHT_STOP, motors)
HL_ls_halt = haltingLimitSwitch("HL_ls_halt", LS_HORIZONTAL_LEFT_STOP, motors)

R_ls_cali = limitSwitch(LS_CALIBRATE_RIGHT)
L_ls_cali = limitSwitch(LS_CALIBRATE_LEFT)
HR_ls_cali = limitSwitch(LS_HORIZONTAL_RIGHT_INIT)
HL_ls_cali = limitSwitch(LS_HORIZONTAL_LEFT_INIT, False)  # Disable Pullup 
