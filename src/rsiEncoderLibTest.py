from rsiEncoder import rsiEncoder
import time


ENCODER_A_PIN = 5
ENCODER_B_PIN = 6


# Setup the encoder
encoder1 = rsiEncoder(ENCODER_A_PIN, ENCODER_B_PIN)

"""
while True:
  last_trigger_time = encoder1.getLastTrigger()
  if last_trigger_time is None:
    last_trigger_time = time.time()  # Use current time as fallback

  tempTime = (time.time() - last_trigger_time) * 1000
  if tempTime > encoder1.getTimeout():
    print("Timeout")
"""

# Keep the script running
input("Press enter to quit\n\n")
