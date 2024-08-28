from encoderv2 import Encoder


ENCODER_1_A = 14                #Pin Label: TXD     Wire Color:Brown
ENCODER_1_B = 15                #Pin Label: RXD     Wire Color:White

ENCODER_2_A = 16                #Pin Label: 16      Wire Color:Brown
ENCODER_2_B = 17                #Pin Label: 17      Wire Color:White

# Initialize Encoders
encoder1 = Encoder(ENCODER_1_A, ENCODER_1_B)
encoder2 = Encoder(ENCODER_2_A, ENCODER_2_B)
encoders = [encoder1, encoder2]

def cleanup():
  for encoder in encoders:
    encoder.close()