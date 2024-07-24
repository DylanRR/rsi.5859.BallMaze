#from rsiEncoder import rsiEncoder
from encoderv2 import Encoder
import time



ENCODER_A_PIN = 5
ENCODER_B_PIN = 6


# Setup the encoder
#encoder1 = rsiEncoder(ENCODER_A_PIN, ENCODER_B_PIN)



"""
while True:
  last_trigger_time = encoder1.getLastTrigger()
  if last_trigger_time is None:
    last_trigger_time = time.time()  # Use current time as fallback

  tempTime = (time.time() - last_trigger_time) * 1000
  if tempTime > encoder1.getTimeout():
    print("Timeout")
"""

timeout = 0.4
minSpeedDelta = 0.06
maxSpeedDelta = 0.001
numOfSpeedSamples = 8000

encoder2 = Encoder(ENCODER_A_PIN, ENCODER_B_PIN)

while True:
  #print(f"Encoder Direction: {encoder1.getEncoderDirection()} Encoder Speed: {encoder1.getEncoderSpeed()}")
  print(f"Encoder Speed: {encoder2.getSpeed()}")
  time.sleep(.1)


"""
encoder = Encoder(ENCODER_A_PIN, ENCODER_B_PIN)
print("Start Spinninng at your fastest speed.")
time.sleep(1)
input("Press ENTER to start recording speed.")
speeds = []
for _ in range(10000):
  # Call getSpeed() and add the result to the list
  speed = encoder.getSpeed()
  speeds.append(speed)

# Calculate the average speed
average_fast_speed = sum(speeds) / len(speeds)
print(f"Average speed over 10k steps: {average_fast_speed}")


print("Now spin the encoder slowly.")
time.sleep(1)
input("Press ENTER to start recording speed.")

slowSpeeds = []
for _ in range(10000):
  # Call getSpeed() and add the result to the list
  speed = encoder.getSpeed()
  slowSpeeds.append(speed)

# Calculate the average speed
average_slow_speed = sum(slowSpeeds) / len(slowSpeeds)
print(f"Average speed over 10k steps: {average_slow_speed}")

print("Gathering Results...")
time.sleep(1)
print(f"Fastest Speed: {average_fast_speed}")
print(f"Slowest Speed: {average_slow_speed}")

encoder.close()




"""