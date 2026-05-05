from Enums.direction import*
from Enums.toggle import*
from Business.pubsub import*
from Enums.event import*

# Manager subscribes to toilet and bed
class Manager(Subscriber):
    def __init__(self, zones = [], bed = None):
        self.zones = zones
        self.direction = Direction.TOILET
        self.inBed = True
        self.bed = bed

    def StartUp(self):
        self.TurnOffAllLight()
        self.SetInBed(False)
        self.bed.StartCheckBed()


    def ShutDown(self):
        self.TurnOffAllLight()
        for zone in self.zones:
            zone.ShutDown()
    

    # What happens when manager receives a message from toilet or bed
    def Receive(self, message):
        if message == Event.ENTER_BED:
            self.ToggleDirection(Direction.TOILET)
            self.SetInBed(True)
            self.TurnOffAllLight()

        elif message == Event.EXIT_BED:
            self.SetInBed(False)

        elif message == Event.ENTER_TOILET:
            self.ToggleDirection(Direction.BED)
            
    # Sets the belief of all zones to same value regarding whether or not
    # the user is in bed 
    def SetInBed(self, value):
        for zone in self.zones:
            zone.userInBed = value

    # Sets the direction of movement for all zones
    def ToggleDirection(self, direction):
        if(self.direction != direction):
            self.direction = direction
            for zone in self.zones:
                temp = zone.nextZone
                zone.nextZone = zone.prevZone
                zone.prevZone = temp
    
    # Turns off light in all zones
    def TurnOffAllLight(self):
        for zone in self.zones:
            zone.ToggleLight(Toggle.OFF)
    