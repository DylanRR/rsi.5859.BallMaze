import staticChips
import  mcp23017_wrapper

#TODO: Fix all the mcp PINS
__breakBeamPin = 8


__ld_IR_pin = 0
__ld_encoder1_pin = 1
__ld_encoder2_pin = 2
__ld_error_pin = 3
__btn_home_pin = 4
__btn_lup_pin = 5
__btn_rup_pin = 6
__btn_recalibrate_pin = 7
__ld_estop_pin = 9
__ld_breakBeam_pin = 10
__ld_homing_pin = 11

Ir_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, __ld_IR_pin)
Encoder1_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, __ld_encoder1_pin)
Encoder2_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, __ld_encoder2_pin)
Error_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, __ld_error_pin)
home_BTN = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, __btn_home_pin)
lup_BTN = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, __btn_lup_pin)
rup_BTN = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, __btn_rup_pin)
recalibrate_BTN = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, __btn_recalibrate_pin)
estop_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, __ld_estop_pin)
breakBeam_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, __ld_breakBeam_pin)
homing_LED = mcp23017_wrapper.MCP_LED(staticChips.mcpObj, __ld_homing_pin)

breakBeam_SENS = mcp23017_wrapper.MCP_BTN(staticChips.mcpObj, __breakBeamPin)

