from adafruit_ads1x15.ads1115 import ADS1115
from ads1115_wrapper import MotorSync
import board
import busio

#Define channels
LEFT_POT = 0
RIGHT_POT = 1

# Initialize the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS1115(i2c, address=0x48)
mSync = MotorSync(ads, LEFT_POT, RIGHT_POT)