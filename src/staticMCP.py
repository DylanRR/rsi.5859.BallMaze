import staticChips
import  mcp23017_wrapper

#TODO: Fix all the mcp PINS
breakBeamPin = 8


ld_IR_pin = 0
ld_encoder1_pin = 1
ld_encoder2_pin = 2
ld_error_pin = 3
btn_home_pin = 4
btn_lup_pin = 5
btn_rup_pin = 6
btn_recalibrate_pin = 7
ld_estop_pin = 9
ld_breakBeam_pin = 10
ls_homing_pin = 11

Ir_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, ld_IR_pin)
Encoder1_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, ld_encoder1_pin)
Encoder2_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, ld_encoder2_pin)
Error_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, ld_error_pin)
home_BTN = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, btn_home_pin)
lup_BTN = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, btn_lup_pin)
rup_BTN = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, btn_rup_pin)
recalibrate_BTN = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, btn_recalibrate_pin)
estop_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, ld_estop_pin)
breakBeam_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, ld_breakBeam_pin)
homing_LS = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, ls_homing_pin)

breakBeam_SENS = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, breakBeamPin, debounce_time=0.0)

