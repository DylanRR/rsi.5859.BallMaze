#from rsiEncoder import rsiEncoder
from encoderv2 import Encoder
import time



ENCODER_A_PIN = 5
ENCODER_B_PIN = 6


# Setup the encoder
#encoder1 = rsiEncoder(ENCODER_A_PIN, ENCODER_B_PIN)
encoder2 = Encoder(ENCODER_A_PIN, ENCODER_B_PIN)

"""
while True:
  last_trigger_time = encoder1.getLastTrigger()
  if last_trigger_time is None:
    last_trigger_time = time.time()  # Use current time as fallback

  tempTime = (time.time() - last_trigger_time) * 1000
  if tempTime > encoder1.getTimeout():
    print("Timeout")
"""
while True:
  #print(f"Encoder Direction: {encoder1.getEncoderDirection()} Encoder Speed: {encoder1.getEncoderSpeed()}")
  print(f"Encoder Count: {encoder2.getValue()} Encoder Direction: {encoder2.direction}")
  time.sleep(.1)
  
# Keep the script running
input("Press enter to quit\n\n")
