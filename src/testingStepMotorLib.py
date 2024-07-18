import rsiStepMotor
from time import sleep
from gpiozero import Button

DIRECTION_PIN = 21
STEP_PIN = 16
ENABLE_PIN = 20
HALT_PIN = 4

motor1 = rsiStepMotor(STEP_PIN, DIRECTION_PIN, ENABLE_PIN)
btnHalt = Button(HALT_PIN, pull_up=True, bounce_time=0.2)

def enableDisableTest():
	motor1.enableMotor()
	sleep(5)
	motor1.disableMotor()
	
def setDirectionTest():
	motor1.setDirection(True)
	sleep(5)
	motor1.setDirection(False)



btnHalt.when_deactivated = motor1.haltMotor("E-Stop Button")
def main():
	try:
		enableDisableTest()
	except Exception as e:
		print(f"Error: {e}")
	finally:
		motor1.haltMotor()


if __name__ == "__main__":
	main()