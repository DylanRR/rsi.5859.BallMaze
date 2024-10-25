from gpiozero import Button

class breakBeam:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.beamBroken, bouncetime=300)

    def beamBroken(self, channel):
        print("Beam Broken")
        # Do something here

    def __del__(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup(self.pin)