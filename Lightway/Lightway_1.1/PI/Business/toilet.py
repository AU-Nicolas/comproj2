from Business.zone import*
from Enums.direction import*
from Enums.event import*
from Business.pubsub import Publisher
from Enums.toggle import*

class Toilet(Zone):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publisher = Publisher()
        
    def SetActive(self):
        self.publisher.Publish(Event.ENTER_TOILET)  
        self.StartCheckIfActive()

    def CheckIfActive(self):
        while (not self.userInBed and self.systemIsActive):
            
            if (not self.IsOccupied() and self.nextZone.IsOccupied()):
                self.ToggleLight(Toggle.OFF)
                self.publisher.Publish(Event.EXIT_TOILET)
                self.nextZone.SetActive()
                return
            else:
                self.ToggleLight(Toggle.ON)
                self.nextZone.ToggleLight(Toggle.ON)
                time.sleep(0.1)

        self.ToggleLight(Toggle.OFF)
        self.nextZone.ToggleLight(Toggle.OFF)
        