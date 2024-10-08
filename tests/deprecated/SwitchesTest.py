from gpiozero import Button, InputDevice, DigitalInputDevice, Device
import atexit
# Close all devices managed by gpiozero
Device.close(12)
Device.close(13)


#GPIO PI Pins
BTN_ESTOP = 0                   #Pin Label: EED     Wire Color: Red
SDA_BUS = 2                     #Pin Label: SDA     Wire Color: Orange
SCL_BUS = 3                     #Pin Label: SCL     Wire Color: Purple
LS_TOP_RIGHT = 4                #Pin Label: 4       Wire Color: Red
LS_BOTTOM_RIGHT = 5             #Pin Label: 5       Wire Color:Red
LS_CALIBRATE_RIGHT = 6          #Pin Label: 6       Wire Color:Red
#LS_TOP_LEFT = 7                 #Pin Label: CE1     Wire Color:Red       Diabled and line tapped into GPIO 1 (EEC)
LS_BOTTOM_LEFT = 1              #Pin Label: CE0     Wire Color:Red        Was Pin 8
LS_CALIBRATE_LEFT = 2           #Pin Label: MISO    Wire Color:Red        Was Pin 9
LS_HORIZONTAL_RIGHT_INIT = 3    #Pin Label: MOSI    Wire Color:Red        Was Pin 10  
LS_HORIZONTAL_RIGHT_STOP = 27   #Pin Label: SCLK    Wire Color:White      Was Pin 11


LS_HORIZONTAL_LEFT_INIT = 12    #Pin Label: 12      Wire Color:Red


LS_HORIZONTAL_LEFT_STOP = 13    #Pin Label: 13      Wire Color:White <---------------------



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


btn_estop = Button(BTN_ESTOP, pull_up=True, bounce_time=0.02)
if btn_estop.value == 0:
  print("Estop Button Pressed")
btn_estop.when_deactivated = lambda: print("Estop Button Pressed")


TR_ls_halt = Button(LS_TOP_RIGHT, pull_up=True, bounce_time=0.02)
BR_ls_halt = Button(LS_BOTTOM_RIGHT, pull_up=True, bounce_time=0.02)
#TL_ls_halt = Button(LS_TOP_LEFT, pull_up=True, bounce_time=0.02)
BL_ls_halt = Button(LS_BOTTOM_LEFT, pull_up=True, bounce_time=0.02)
R_ls_cali = Button(LS_CALIBRATE_RIGHT, pull_up=True, bounce_time=0.02)
L_ls_cali = Button(LS_CALIBRATE_LEFT, pull_up=True, bounce_time=0.02)
HR_ls_halt = Button(LS_HORIZONTAL_RIGHT_STOP, bounce_time=0.02)
HR_ls_cali = Button(LS_HORIZONTAL_RIGHT_INIT, bounce_time=0.02)

HL_ls_halt = Button(LS_HORIZONTAL_LEFT_STOP, bounce_time=0.02)    #<------------------

HL_ls_cali = Button(LS_HORIZONTAL_LEFT_INIT, bounce_time=0.02)

TR_ls_halt.when_deactivated = lambda: print("Top Right Limit Switch Pressed")
#TL_ls_halt.when_deactivated = lambda: print("Top Left Limit Switch Pressed")
BR_ls_halt.when_deactivated = lambda: print("Bottom Right Limit Switch Pressed")
BL_ls_halt.when_deactivated = lambda: print("Bottom Left Limit Switch Pressed")
R_ls_cali.when_deactivated = lambda: print("Right Calibration Limit Switch Pressed")
L_ls_cali.when_deactivated = lambda: print("Left Calibration Limit Switch Pressed")
HR_ls_halt.when_deactivated = lambda: print("Horizontal Right Halt Limit Switch Pressed")
HL_ls_halt.when_deactivated= lambda: print("Horizontal Left Halt Limit Switch Pressed")
HR_ls_cali.when_deactivated = lambda: print("Horizontal Right Calibration Limit Switch Pressed")
HL_ls_cali.when_deactivated = lambda: print("Horizontal Left Calibration Limit Switch Pressed")


# Wait for user to press Enter to quit
input("Press Enter End Test...")
# Close all GPIO resources at the end
btn_estop.close()
TR_ls_halt.close()
BR_ls_halt.close()
#TL_ls_halt.close()
BL_ls_halt.close()
R_ls_cali.close()
L_ls_cali.close()

HR_ls_halt.close()
HR_ls_cali.close()
HL_ls_halt.close()
HL_ls_cali.close()
# Close all devices managed by gpiozero
Device.close(btn_estop)
Device.close(TR_ls_halt)
Device.close(BR_ls_halt)
Device.close(TL_ls_halt)
Device.close(BL_ls_halt)
Device.close(R_ls_cali)
Device.close(L_ls_cali)
Device.close(HR_ls_halt)
Device.close(HR_ls_cali)
Device.close(HL_ls_halt)
Device.close(HL_ls_cali)


