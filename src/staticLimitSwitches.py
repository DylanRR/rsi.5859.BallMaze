from limitSwitch import haltingLimitSwitch, limitSwitch

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

# Initialize Haulting Limit Switches
btn_estop = haltingLimitSwitch("btn_estop", BTN_ESTOP)
TR_ls_halt = haltingLimitSwitch("TR_ls_halt", LS_TOP_RIGHT)
BR_ls_halt = haltingLimitSwitch("BR_ls_halt", LS_BOTTOM_RIGHT)
TL_ls_halt = haltingLimitSwitch("TL_ls_halt", LS_TOP_LEFT)  #NOTE: May need to turn of the pullup resistor
BL_ls_halt = haltingLimitSwitch("BL_ls_halt", LS_BOTTOM_LEFT)
HR_ls_halt = haltingLimitSwitch("HR_ls_halt", LS_HORIZONTAL_RIGHT_STOP)
HL_ls_halt = haltingLimitSwitch("HL_ls_halt", LS_HORIZONTAL_LEFT_STOP)
haltingLimitSwitches = [btn_estop, TR_ls_halt, BR_ls_halt, TL_ls_halt, BL_ls_halt, HR_ls_halt, HL_ls_halt]

# Initialize Limit Switches
R_ls_cali = limitSwitch(LS_CALIBRATE_RIGHT)
L_ls_cali = limitSwitch(LS_CALIBRATE_LEFT)
HR_ls_cali = limitSwitch(LS_HORIZONTAL_RIGHT_INIT)
HL_ls_cali = limitSwitch(LS_HORIZONTAL_LEFT_INIT)
limitSwitches = [R_ls_cali, L_ls_cali, HR_ls_cali, HL_ls_cali]


#Object cleanup
def cleanup():
  for switch in haltingLimitSwitches:
    switch.close()
  for switch in limitSwitches:
    switch.close()







