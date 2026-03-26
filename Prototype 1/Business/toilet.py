from Business.zone import*
from Enums.direction import*

class Toilet(Zone):
    def SetActive(self):
        self.ToggleLight(Toggle.ON)
        self.controller.ToggleDirection(Direction.BED)
        self.nextZone.ToggleLight(Toggle.ON)
        self.StartCheckIfActive()
        