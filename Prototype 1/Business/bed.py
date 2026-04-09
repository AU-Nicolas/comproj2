from Business.zone import*
from Enums.direction import*
from Enums.toggle import*
import time
import threading

class Bed(Zone):
    def __init__(self, *args, dormant_time = 2, **kwargs):
        super().__init__(*args, **kwargs)
        self.dormant_time = dormant_time
        self.start_time = time.time()

    # Sets the bed zone to active.
    def SetActive(self):
        print("The bed is active")
        self.manager.TurnOffAllLight()
        self.ToggleLight(Toggle.ON)
        self.manager.ToggleDirection(Direction.TOILET)
        self.manager.inBed = True
        self.StartCheckIfActive()

    def CheckIfActive(self):
        while (True):
            if (not self.IsOccupied()):
                
                if (self.nextZone.IsOccupied()):
                    self.ToggleLight(Toggle.OFF)
                    self.manager.inBed = False
                    self.StartCheckBed()
                    self.nextZone.SetActive()
                    break
                else:
                    if time.time() - self.start_time > self.dormant_time:
                        self.ToggleLight(self.ToggleLight(Toggle.OFF))
                        self.nextZone.ToggleLight(Toggle.OFF)
                    time.sleep(1)
            else:
                self.start_time = time.time()
                self.ToggleLight(Toggle.ON)
                self.nextZone.ToggleLight(Toggle.ON)
                time.sleep(1)
        

    def StartCheckBed(self):
        thread = threading.Thread(
            target = self.CheckBed,
            daemon = True
        )
        thread.start
        
    # Check if a person is in the bed zone, using isOccupied from sensors
    def CheckBed(self):
        while(not self.manager.inBed):
            if(self.IsOccupied()):
                self.manager.inBed = True
                self.SetActive()
            else:
                time.sleep(1)

    
