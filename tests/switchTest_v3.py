from gpiozero import Button, DigitalOutputDevice

#GPIO PI Pins
BTN_ESTOP = 4                   #Pin Label: 4       Wire Color: Black
SDA_BUS = 2                     #Pin Label: SDA     Wire Color: Orange
SCL_BUS = 3                     #Pin Label: SCL     Wire Color: Purple
LS_TOP_RIGHT = 9                #Pin Label: MISO    Wire Color: White
LS_BOTTOM_RIGHT = 22            #Pin Label: 22      Wire Color:Brown
LS_CALIBRATE_RIGHT = 10         #Pin Label: MOSI    Wire Color:Purple
LS_TOP_LEFT = 5                 #Pin Label: 5       Wire Color:Green/Yellow
LS_BOTTOM_LEFT = 11             #Pin Label: SCLK    Wire Color:Gray
LS_CALIBRATE_LEFT = 0           #Pin Label: ID_SD   Wire Color:Blue
LS_HORIZONTAL_RIGHT_INIT = 17   #Pin Label: 17      Wire Color:Blue
LS_HORIZONTAL_RIGHT_STOP = 27   #Pin Label: 27      Wire Color:Green
LS_HORIZONTAL_LEFT_INIT = 13    #Pin Label: 13      Wire Color:Gray
LS_HORIZONTAL_LEFT_STOP = 6     #Pin Label: 6       Wire Color:Brown
ENCODER_1_A = 16                #Pin Label: 16      Wire Color:Blue/Green
ENCODER_1_B = 12                #Pin Label: 12      Wire Color:White/Orange
ENCODER_2_A = 21                #Pin Label: 21      Wire Color:Blue/Purple
ENCODER_2_B = 20                #Pin Label: 20      Wire Color:White/Blue
MOTOR_1_ENABLE = 14             #Pin Label: TXD     Wire Color:White
MOTOR_1_DIRECTION = 15          #Pin Label: RXD     Wire Color:Green
MOTOR_1_STEP = 18               #Pin Label: 18      Wire Color:Brown
MOTOR_2_ENABLE = 23             #Pin Label: 23      Wire Color:White
MOTOR_2_DIRECTION = 24          #Pin Label: 24      Wire Color:Green
MOTOR_2_STEP = 25               #Pin Label: 25      Wire Color:Brown
MOTOR_3_ENABLE = 8              #Pin Label: CE0     Wire Color:White
MOTOR_3_DIRECTION = 7           #Pin Label: CE1     Wire Color:Green
MOTOR_3_STEP = 1                #Pin Label: EEC     Wire Color:Brown


btn_estop = Button(BTN_ESTOP, pull_up=True, bounce_time=0.02)
TR_ls_halt = Button(LS_TOP_RIGHT, pull_up=True, bounce_time=0.02)
BR_ls_halt = Button(LS_BOTTOM_RIGHT, pull_up=True, bounce_time=0.02)
TL_ls_halt = Button(LS_TOP_LEFT, pull_up=True, bounce_time=0.02)
BL_ls_halt = Button(LS_BOTTOM_LEFT, pull_up=True, bounce_time=0.02)
R_ls_cali = Button(LS_CALIBRATE_RIGHT, pull_up=True, bounce_time=0.02)
L_ls_cali = Button(LS_CALIBRATE_LEFT, pull_up=True, bounce_time=0.02)
HR_ls_halt = Button(LS_HORIZONTAL_RIGHT_STOP, pull_up=True, bounce_time=0.02)
HR_ls_cali = Button(LS_HORIZONTAL_RIGHT_INIT, pull_up=True, bounce_time=0.02)
HL_ls_halt = Button(LS_HORIZONTAL_LEFT_STOP, pull_up=True, bounce_time=0.02)
HL_ls_cali = Button(LS_HORIZONTAL_LEFT_INIT, pull_up=True, bounce_time=0.02)

btn_estop.when_deactivated = lambda: print("Estop Button Pressed")
TR_ls_halt.when_deactivated = lambda: print("Top Right Limit Switch Pressed")
TL_ls_halt.when_deactivated = lambda: print("Top Left Limit Switch Pressed")
BR_ls_halt.when_deactivated = lambda: print("Bottom Right Limit Switch Pressed")
BL_ls_halt.when_deactivated = lambda: print("Bottom Left Limit Switch Pressed")
R_ls_cali.when_deactivated = lambda: print("Right Calibration Limit Switch Pressed")
L_ls_cali.when_deactivated = lambda: print("Left Calibration Limit Switch Pressed")
HR_ls_halt.when_deactivated = lambda: print("Horizontal Right Halt Limit Switch Pressed")
HL_ls_halt.when_deactivated= lambda: print("Horizontal Left Halt Limit Switch Pressed")
HR_ls_cali.when_deactivated = lambda: print("Horizontal Right Calibration Limit Switch Pressed")
HL_ls_cali.when_deactivated = lambda: print("Horizontal Left Calibration Limit Switch Pressed")



m1Enable = DigitalOutputDevice(MOTOR_1_ENABLE)
m1Direction = DigitalOutputDevice(MOTOR_1_DIRECTION)
m1Step = DigitalOutputDevice(MOTOR_1_STEP)

m2Enable = DigitalOutputDevice(MOTOR_2_ENABLE)
m2Direction = DigitalOutputDevice(MOTOR_2_DIRECTION)
m2Step = DigitalOutputDevice(MOTOR_2_STEP)

m3Enable = DigitalOutputDevice(MOTOR_3_ENABLE)
m3Direction = DigitalOutputDevice(MOTOR_3_DIRECTION)
m3Step = DigitalOutputDevice(MOTOR_3_STEP)


motor_map = {
    "1": {"enable": m1Enable, "direction": m1Direction, "step": m1Step},
    "2": {"enable": m2Enable, "direction": m2Direction, "step": m2Step},
    "3": {"enable": m3Enable, "direction": m3Direction, "step": m3Step}
}

while True:
  uInput = input("Enter a Motor Number to Test OR Enter 'q' to Quit: ")
  if uInput == "q":
    break
  elif uInput in motor_map:
    uInput2 = input("Enter 1 = Enable, 2 = Direction, 3 = Step: ")
    action_map = {"1": "enable", "2": "direction", "3": "step"}
    if uInput2 in action_map:
      motor = motor_map[uInput][action_map[uInput2]]
      if motor.value == 0:
        motor.on()
        print(f"Motor {uInput} {action_map[uInput2].capitalize()} On")
      else:
        motor.off()
        print(f"Motor {uInput} {action_map[uInput2].capitalize()} Off")


# Wait for user to press Enter to quit
input("Press Enter End Test...")
# Close all GPIO resources at the end
btn_estop.close()
TR_ls_halt.close()
BR_ls_halt.close()
TL_ls_halt.close()
BL_ls_halt.close()
R_ls_cali.close()
L_ls_cali.close()
HR_ls_halt.close()
HR_ls_cali.close()
HL_ls_halt.close()
HL_ls_cali.close()
m1Enable.close()
m1Direction.close()
m1Step.close()
m2Enable.close()
m2Direction.close()
m2Step.close()
m3Enable.close()
m3Direction.close()
m3Step.close()



