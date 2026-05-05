from Enums.direction import*
from Enums.toggle import*

class Manager:
    def __init__(self, zones = []):
        self.zones = zones
        self.direction = Direction.TOILET
        self.inBed = True


    def ToggleDirection(self, direction):
        if(self.direction != direction):
            self.direction = direction
            for zone in self.zones:
                temp = zone.nextZone
                zone.nextZone = zone.prevZone
                zone.prevZone = temp
    
    def TurnOffAllLight(self):
        for zone in self.zones:
            zone.ToggleLight(Toggle.OFF)
    