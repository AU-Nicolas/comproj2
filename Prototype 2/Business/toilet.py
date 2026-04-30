from Business.zone import*
from Enums.direction import*
from Enums.event import*

class Toilet(Zone):
    def __init__(self, *args, logger, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        
    def SetActive(self):
        self.ToggleLight(Toggle.ON)
        self.manager.ToggleDirection(Direction.BED)
        self.nextZone.ToggleLight(Toggle.ON)
        self.logger.RegisterEvent(Event.ENTER_TOILET)  
        self.StartCheckIfActive()

    def CheckIfActive(self):
        while (not self.manager.inBed):
            
            if (not self.IsOccupied() and self.nextZone.IsOccupied()):
                self.ToggleLight(Toggle.OFF)
                self.nextZone.SetActive()
                self.logger.RegisterEvent(Event.EXIT_TOILET)
                break
            else:
                time.sleep(0.1)
        