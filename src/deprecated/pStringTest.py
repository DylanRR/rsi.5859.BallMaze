import board
import busio
import ads1115_wrapper
from adafruit_ads1x15.ads1115 import ADS1115
import time

leftPString = 0
rightPString = 1

# Initialize the I2C bus
print("Initializing I2C bus...")
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C bus initialized.")

# Create an ADS object
print("Creating ADS object...")
ads = ADS1115(i2c, address=0x48)
print("ADS object created.")

# Create an ADS_CHANNEL object
print("Creating ADS_CHANNEL objects...")
leftChannel = ads1115_wrapper.ADS_CHANNEL(ads, leftPString, useSmoothing=True, bufferSize=3)
rightChannel = ads1115_wrapper.ADS_CHANNEL(ads, rightPString, useSmoothing=True, bufferSize=3)
print("ADS_CHANNEL objects created.")

while True:
    leftVal = leftChannel.getValue()
    rightVal = rightChannel.getValue()
    print("Left: ", leftVal, " Right: ", rightVal)
    time.sleep(0.001)