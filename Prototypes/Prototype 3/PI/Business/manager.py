import threading
from Enums.direction import*
from Enums.toggle import*
from Business.pubsub import*
from Enums.event import*
from Business.timestamp import TimeStamp            



# Manager subscribes to toilet and bed
class Manager(Subscriber):
    def __init__(self, 
                 startTime = TimeStamp(22,0),
                 endTime = TimeStamp(9,0),
                 zones = [],
                 bed = None):
        self.startTime = startTime
        self.endTime = endTime
        self.zones = zones
        self.bed = bed
        self.direction = Direction.TOILET
        self.inBed = True
        self.deactivateSystemTimer = None
        self.activateSystemTimer = None
    
    # Starts the system
    def InitializeSystem(self):
        now = TimeStamp.now()
        now.print()
        self.startTime.print()
        self.endTime.print()
        # If the system shouldn't be active
        if (self.startTime < self.endTime and self.startTime <= now and now < self.endTime or 
            self.startTime > self.endTime and (now < self.endTime or now >= self.startTime)):
            self.ActivateSystem()
        else:
            self.DeactivateSystem()
            
    
    def DeactivateSystem(self):
        print("Manager: I try to deactivate the system")
        # Turning off all light
        self.TurnOffAllLight()

        # Setting the system as inactive for all zones
        self.SetSystemActivity(False)

        # Calculates time until the system should be active again
        delta = TimeStamp.now() - self.startTime
        seconds = delta.second + delta.minute*60 + delta.hour*3600
        print(f"Manager: There must pass {seconds} seconds before the system is activated")
        # Activates system when time reaches starttime
        if self.activateSystemTimer:
            self.activateSystemTimer.cancel()
            self.activateSystemTimer = None
        self.activateSystemTimer = threading.Timer(
            interval=seconds,
            function=self.ActivateSystem
        )
        self.activateSystemTimer.daemon = True
        self.activateSystemTimer.start()

    def ActivateSystem(self):
        print("Manager: I activate the system")
        # Setting system as active for all zones
        self.SetSystemActivity(True)

        # Starting monitoring in bedroom
        self.SetInBed(False)
        self.bed.StartCheckBed()

        # Calculates time until the system should be active again
        delta = TimeStamp.now() - self.endTime
        seconds = delta.second + delta.minute*60 + delta.hour*3600
        print(f"Manager: There must pass {seconds} seconds before the system is deactivated")
        # Activates system when time reaches starttime
        if self.deactivateSystemTimer:
            self.deactivateSystemTimer.cancel()
            self.deactivateSystemTimer = None
        self.deactivateSystemTimer = threading.Timer(
            interval=seconds,
            function=self.DeactivateSystem,
        )
        self.deactivateSystemTimer.daemon = True
        self.deactivateSystemTimer.start()


    def SetSystemActivity(self, value):
        for zone in self.zones:
            zone.systemIsActive = value


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
    