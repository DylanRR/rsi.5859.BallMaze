import staticVars as sVars

#Disable all motors
def disableAllMotors():
  for index, motor in enumerate(sVars.motors, start=1):
    motor.haltMotor(f"Motor {index}")

#Object cleanup
def cleanup():
  for motor in sVars.motors:
    motor.close()
  for switch in sVars.haltingLimitSwitches:
    switch.close()
  for switch in sVars.limitSwitches:
    switch.close()
  for encoder in sVars.encoders:
    encoder.close()
