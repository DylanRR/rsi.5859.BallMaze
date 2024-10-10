from rsiStepMotorv2 import rsiDuelStepMotor as duelMotor
import threading

m1Step = 18
m1Dir = 15
m1Enable = 14

m2Step = 1
m2Dir = 7
m2Enable = 8


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