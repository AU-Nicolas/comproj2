from Business.zone import*
from Enums.direction import*
from Enums.event import*
from Enums.toggle import*
import time
import threading
from Business.pubsub import Publisher

class Bed(Zone):
    def __init__(self, *args, dormant_time = 30, **kwargs):
        super().__init__(*args, **kwargs)
        self.dormant_time = dormant_time
        self.start_time = time.time()
        self.publisher = Publisher()

    # Sets the bed zone to active.
    def SetActive(self):
        print("Bed: I run SetActive")
        self.publisher.Publish(Event.ENTER_BED)
        self.StartWhileActive()

    def WhileActive(self):
        while (self.systemIsActive):
            # If no movement is seen inside the bed zone
            if (not self.IsOccupied()):
                # If the beboer has moved to the next zone, that
                # zone is set as active
                if (self.nextZone.IsOccupied()):
                    self.ToggleLight(Toggle.OFF)
                    self.publisher.Publish(Event.EXIT_BED)
                    self.StartCheckBed()
                    self.nextZone.SetActive()
                    return
                else:
                    # If no movement is seen anywhere, all light is turned off
                    if time.time() - self.start_time > self.dormant_time:
                        self.ToggleLight(Toggle.OFF)
                        self.nextZone.ToggleLight(Toggle.OFF)
                    time.sleep(0.1)
            # If we do see movement in the bed zone, we stay here and keep the
            # light on
            else:
                self.start_time = time.time()
                self.ToggleLight(Toggle.ON)
                self.nextZone.ToggleLight(Toggle.ON)
                time.sleep(0.1)

        # We make sure to turn off all the light, when the loop condition is broken,
        # i.e. the system is not active anymore
        self.ToggleLight(Toggle.OFF)
        self.nextZone.ToggleLight(Toggle.OFF)
        

    def StartCheckBed(self):
        thread = threading.Thread(
            target = self.CheckBed,
            daemon = True
        )
        thread.start()
        
    # Check if a person is in the bed zone, using isOccupied from sensors
    def CheckBed(self):
        print("Bed: I run checkBed")
        while(not self.userInBed and self.systemIsActive):
            # If we see movement in the bedroom, we assume the beboer has moved
            # back to the bedroom
            if(self.IsOccupied()):
                self.SetActive()
            else:
                time.sleep(0.1)
        print(f"Bed: I no longer checkBed. user in bed: {self.userInBed}, systemIsActive: {self.systemIsActive}")

    
