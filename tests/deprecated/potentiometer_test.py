import smbus2
import time

# Get I2C bus
bus = smbus2.SMBus(1)

# ADS7828 address, 0x48(72)
address = 0x48

# Voltage range
VOLTAGE_RANGE = 3.18

def read_adc():
    try:
        # Send command byte to select channel 0 and turn on the A/D converter
        command_byte = 0x84  # Single-ended input on channel 0, power-down between conversions
        bus.write_byte(address, command_byte)

        time.sleep(0.1)  # Delay to allow conversion to complete

        # Read 2 bytes of data from the ADS7828
        data = bus.read_i2c_block_data(address, 0x00, 2)

        # Debug: Print raw data bytes
        print(f"Raw data bytes: {data}")

        # Convert the data to 12-bits
        raw_adc = ((data[0] << 8) + data[1]) & 0x0FFF

        return raw_adc
    except Exception as e:
        print(f"Read error: {e}")
        return None

while True:
    raw_adc = read_adc()
    if raw_adc is not None:
        # Convert raw ADC value to voltage
        voltage = (raw_adc / 4095.0) * VOLTAGE_RANGE

        # Output data to screen
        print(f"Digital value of analog input: {raw_adc}, Voltage: {voltage:.2f} V")
    else:
        print("Failed to read ADC value.")
    
    time.sleep(0.5)  # Adjust the delay as needed