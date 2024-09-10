from adafruit_ads1x15.ads1115 import ADS1115
from ads1115_wrapper import ADS_CHANNEL, MotorSync

#Define channels
LEFT_POT = 0
RIGHT_POT = 1

ads = ADS1115(i2c)
mSync = MotorSync(ads, LEFT_POT, RIGHT_POT)