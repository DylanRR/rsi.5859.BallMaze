import mcp23017_wrapper
from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_ads1x15.ads1115 import ADS1115
import ads1115_wrapper

import board
import busio
import time

# Create I2C bus object
i2c = busio.I2C(board.SCL, board.SDA)

# Create an instance of the MCP23017 class
mcpObj = MCP23017(i2c, address=0x20)

ld_ir = mcp23017_wrapper.MCP_LED(mcpObj, 0)
ld_encoder1 = mcp23017_wrapper.MCP_LED(mcpObj, 1)
ld_encoder2 = mcp23017_wrapper.MCP_LED(mcpObj, 2)
ld_error = mcp23017_wrapper.MCP_LED(mcpObj, 3)
ld_estop = mcp23017_wrapper.MCP_LED(mcpObj, 9)
ls_sens = mcp23017_wrapper.MCP_LED(mcpObj, 10)
ld_homeing = mcp23017_wrapper.MCP_LED(mcpObj, 11)

leds = {
    "ld_ir": ld_ir,
    "ld_encoder1": ld_encoder1,
    "ld_encoder2": ld_encoder2,
    "ld_error": ld_error,
    "ld_estop": ld_estop,
    "ls_sens": ls_sens,
    "ld_homeing": ld_homeing
}

# Button setup using gpiozero
btn_home = mcp23017_wrapper.MCP_BTN(mcpObj, 4)
btn_lup = mcp23017_wrapper.MCP_BTN(mcpObj, 5)
btn_rup = mcp23017_wrapper.MCP_BTN(mcpObj, 6)
btn_recalibrate = mcp23017_wrapper.MCP_BTN(mcpObj, 7)

buttons = {
    "btn_home": btn_home,
    "btn_lup": btn_lup,
    "btn_rup": btn_rup,
    "btn_recalibrate": btn_recalibrate
}

def test_buttons():
  print("Press any button to test the button functionality")
  while True:
    for name, button in buttons.items():
      if button.is_pressed():
        print(f"Button {name} is pressed")
        button.reset()  # Reset the pressed state
    time.sleep(0.1)  # Add a small delay to avoid spamming the output

def test_leds():
  for name, led in leds.items():
    input("Press Enter to turn on the next LED")
    print(f"Turning ON LED {name}")
    led.turnOn()


adsObj = ADS1115(i2c)
pot1 = ads1115_wrapper.ADS_CHANNEL(adsObj, 0)
pot2 = ads1115_wrapper.ADS_CHANNEL(adsObj, 1)

def test_ads():
  while True:
    print(f"Pot1: {pot1.getValue()}V Pot2: {pot2.getValue()}V")
    time.sleep(0.1)







def main():
  #test_leds()
  #test_buttons()
  test_ads()

if __name__ == "__main__":
  main()

