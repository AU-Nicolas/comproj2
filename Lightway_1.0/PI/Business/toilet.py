from Business.zone import*
from Enums.direction import*
from Enums.event import*
from Business.pubsub import Publisher

class Toilet(Zone):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publisher = Publisher()
        
    def SetActive(self):
        self.ToggleLight("ON")
        self.nextZone.ToggleLight("ON")
        self.publisher.Publish(Event.ENTER_TOILET)  
        self.StartCheckIfActive()

    def CheckIfActive(self):
        while (not self.userInBed and self.systemIsActive):
            
            if (not self.IsOccupied() and self.nextZone.IsOccupied()):
                self.ToggleLight("OFF")
                self.nextZone.SetActive()
                self.publisher.Publish(Event.EXIT_TOILET)
                break
            else:
                time.sleep(0.1)
        self.ToggleLight("OFF")
        