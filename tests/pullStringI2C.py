import time
import board
import adafruit_ads7830.ads7830 as ADC
from adafruit_ads7830.analog_in import AnalogIn
i2c = board.I2C()

# Initialize ADS7830
adc = ADC.ADS7830(i2c)
chan = AnalogIn(adc, 0)


while True:
    print(f"ADC channel 0 = {adc.read(0)}")
    time.sleep(0.1)