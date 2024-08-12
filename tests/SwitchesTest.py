from gpiozero import Button

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


btn_estop = Button(BTN_ESTOP, pull_up=True, bounce_time=0.2)

TR_ls_halt = Button(LS_TOP_RIGHT, pull_up=True)
BR_ls_halt = Button(LS_BOTTOM_RIGHT, pull_up=True)

TL_ls_halt = Button(LS_TOP_LEFT, pull_up=True)
BL_ls_halt = Button(LS_BOTTOM_LEFT, pull_up=True)

HR_ls_halt = Button(LS_HORIZONTAL_RIGHT_STOP, pull_up=True)
HL_ls_halt = Button(LS_HORIZONTAL_LEFT_STOP, pull_up=True)

R_ls_cali = Button(LS_CALIBRATE_RIGHT, pull_up=True)
L_ls_cali = Button(LS_CALIBRATE_LEFT, pull_up=True)
HR_ls_cali = Button(LS_HORIZONTAL_RIGHT_INIT, pull_up=True)
HL_ls_cali = Button(LS_HORIZONTAL_LEFT_INIT, pull_up=True)


btn_estop.when_pressed = lambda: print("Estop Button Pressed")
TR_ls_halt.when_pressed = lambda: print("Top Right Limit Switch Pressed")
BR_ls_halt.when_pressed = lambda: print("Bottom Right Limit Switch Pressed")
TL_ls_halt.when_pressed = lambda: print("Top Left Limit Switch Pressed")
BL_ls_halt.when_pressed = lambda: print("Bottom Left Limit Switch Pressed")
HR_ls_halt.when_pressed = lambda: print("Horizontal Right Halt Limit Switch Pressed")
HL_ls_halt.when_pressed = lambda: print("Horizontal Left Halt Limit Switch Pressed")
R_ls_cali.when_pressed = lambda: print("Horizontal Right Calibration Limit Switch Pressed")
L_ls_cali.when_pressed = lambda: print("Horizontal Left Calibration Limit Switch Pressed")

# Wait for user to press Enter to quit
input("Press Enter End Test...")
