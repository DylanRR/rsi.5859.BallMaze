from gpiozero import MCP3008
from time import sleep

# Define the channel numbers for the potentiometers
POTENTIOMETER_CH0 = 0
POTENTIOMETER_CH1 = 1

# Set up the MCP3008 ADC
adc0 = MCP3008(channel=POTENTIOMETER_CH0)
adc1 = MCP3008(channel=POTENTIOMETER_CH1)

# Read the value from a potentiometer
def read_potentiometer(adc):
    return adc.value * 1023

# Main function
def main():
    prev_value_0 = read_potentiometer(adc0)
    prev_value_1 = read_potentiometer(adc1)

    try:
        while True:
            # Read current values from the potentiometers
            current_value_0 = read_potentiometer(adc0)
            current_value_1 = read_potentiometer(adc1)

            # Check for changes and print if there is a change
            if current_value_0 != prev_value_0:
                print("Potentiometer 0 value:", current_value_0)
                prev_value_0 = current_value_0

            if current_value_1 != prev_value_1:
                print("Potentiometer 1 value:", current_value_1)
                prev_value_1 = current_value_1

            # Delay to allow time for the ADC to settle
            sleep(0.1)
    except KeyboardInterrupt:
        pass

# Run the main function
if __name__ == "__main__":
    main()