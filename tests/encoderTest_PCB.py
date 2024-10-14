from encoderv2 import Encoder
import time

ENCODER_1_A = 7                #Pin Label: 16      Wire Color:Blue/Green
ENCODER_1_B = 1                #Pin Label: 12      Wire Color:White/Orange
ENCODER_2_A = 25                #Pin Label: 21      Wire Color:Blue/Purple
ENCODER_2_B = 8                #Pin Label: 20      Wire Color:White/Blue


# Initialize Encoders
encoder1 = Encoder(ENCODER_1_A, ENCODER_1_B)
encoder2 = Encoder(ENCODER_2_A, ENCODER_2_B)
encoders = [encoder1, encoder2]

def cleanup():
  for encoder in encoders:
    encoder.close()


def main():
  try:
    while True:
      print (f"Encoder 1 Dir: {encoder1.direction} Encoder 2 Dir: {encoder2.direction}")
      time.sleep(0.1)
  except KeyboardInterrupt:
    print("Exiting...")
  finally:
    cleanup()

if __name__ == "__main__":
  main()