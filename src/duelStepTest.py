from rsiStepMotorv2 import rsiDuelStepMotor as duelMotor
import threading

m1Step = 17
m1Dir = 27
m1Enable = 22

m2Step = 23
m2Dir = 24
m2Enable = 25

vMotors = duelMotor()
vMotors.initMotor1(m1Step, m1Dir, m1Enable)
vMotors.initMotor2(m2Step, m2Dir, m2Enable)

KillFlag = False

def run():
  global KillFlag
  vMotors.pulseFactory(not KillFlag, True)


def main():
    global KillFlag
    input("Press Enter to start...")
    thread = threading.Thread(target=run)
    thread.start()
    vMotors.setTargetSpeed(50)

    input("Press Enter to stop...")
    KillFlag = True
    thread.join()  # Wait for the thread to finish

    # Ensure motors are properly disabled or cleaned up
    vMotors.disableMotors()
    vMotors.close()

if __name__ == "__main__":
    main()