from gpiozero import Button

class breakBeam:
    def __init__(self, mcpObj, pin):
        self.pin = pin
        self.mcp = mcpObj

    def beamBroken(self, channel):
        print("Beam Broken")
        # Do something here

    def __del__(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup(self.pin)