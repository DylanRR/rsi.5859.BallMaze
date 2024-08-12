from time import sleep
from encoderv2 import Encoder


#GPIO PI Pins
BTN_ESTOP = 0                   #Pin Label: EED     Wire Color: Red
SDA_BUS = 2                     #Pin Label: SDA     Wire Color: Orange
SCL_BUS = 3                     #Pin Label: SCL     Wire Color: Purple
LS_TOP_RIGHT = 4                #Pin Label: 4       Wire Color: Red
LS_BOTTOM_RIGHT = 5             #Pin Label: 5       Wire Color:Red
LS_CALIBRATE_RIGHT = 6          #Pin Label: 6       Wire Color:Red
LS_TOP_LEFT = 7                 #Pin Label: CE1     Wire Color:Red
LS_BOTTOM_LEFT = 8              #Pin Label: CE0     Wire Color:Red
LS_CALIBRATE_LEFT = 9           #Pin Label: MISO    Wire Color:Red
LS_HORIZONTAL_RIGHT_STOP = 10   #Pin Label: MOSI    Wire Color:White
LS_HORIZONTAL_RIGHT_INIT = 11   #Pin Label: SCLK    Wire Color:Red
LS_HORIZONTAL_LEFT_STOP = 12    #Pin Label: 12      Wire Color:White
LS_HORIZONTAL_LEFT_INIT = 13    #Pin Label: 13      Wire Color:Red
ENCODER_1_A = 14                #Pin Label: TXD     Wire Color:Brown
ENCODER_1_B = 15                #Pin Label: RXD     Wire Color:White
ENCODER_2_A = 16                #Pin Label: 16      Wire Color:Brown
ENCODER_2_B = 17                #Pin Label: 17      Wire Color:White
MOTOR_2_ENABLE = 18             #Pin Label: 18      Wire Color:White
MOTOR_2_DIRECTION = 19          #Pin Label: 19      Wire Color:Green
MOTOR_2_STEP = 20               #Pin Label: 20      Wire Color:Brown
MOTOR_1_ENABLE = 21             #Pin Label: 21      Wire Color:White
MOTOR_1_DIRECTION = 22          #Pin Label: 22      Wire Color:Green
MOTOR_1_STEP = 23               #Pin Label: 23      Wire Color:Brown
MOTOR_3_ENABLE = 24             #Pin Label: 24      Wire Color:White
MOTOR_3_DIRECTION = 25          #Pin Label: 25      Wire Color:Green
MOTOR_3_STEP = 26               #Pin Label: 26      Wire Color:Brown

encoder1 = Encoder(ENCODER_1_A, ENCODER_1_B)
encoder2 = Encoder(ENCODER_2_A, ENCODER_2_B)

def main():
	while True:
		if encoder1.direction is not None:
			print(f"Encoder 1 Direction: {encoder1.direction} Speed: {encoder1.__speed}")
		if encoder2.direction is not None:
			print(f"Encoder 2 Direction: {encoder2.direction} Speed: {encoder2.__speed}")
		sleep(1)

if __name__ == "__main__":
	main()
