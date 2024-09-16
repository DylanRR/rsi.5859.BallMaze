from encoderv2 import Encoder


ENCODER_1_A = 16                #Pin Label: 16      Wire Color:Blue/Green
ENCODER_1_B = 12                #Pin Label: 12      Wire Color:White/Orange
ENCODER_2_A = 21                #Pin Label: 21      Wire Color:Blue/Purple
ENCODER_2_B = 20                #Pin Label: 20      Wire Color:White/Blue

# Initialize Encoders
encoder1 = Encoder(ENCODER_1_A, ENCODER_1_B)
encoder2 = Encoder(ENCODER_2_A, ENCODER_2_B)
encoders = [encoder1, encoder2]

def cleanup():
  for encoder in encoders:
    encoder.close()