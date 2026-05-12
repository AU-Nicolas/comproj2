from Business.zone import*
from Enums.direction import*
from Enums.event import*
import time
import threading
from Business.pubsub import Publisher

class Bed(Zone):
    def __init__(self, *args, dormant_time = 2, **kwargs):
        super().__init__(*args, **kwargs)
        self.dormant_time = dormant_time
        self.start_time = time.time()
        self.publisher = Publisher()

    # Sets the bed zone to active.
    def SetActive(self):
        print("Bed: I run SetActive")
        self.publisher.Publish(Event.ENTER_BED)
        self.ToggleLight("ON")
        self.nextZone.ToggleLight("ON")
        
        self.StartCheckIfActive()

    def CheckIfActive(self):
        while (self.systemIsActive):
            if (not self.IsOccupied()):
                
                if (self.nextZone.IsOccupied()):
                    self.ToggleLight("OFF")
                    self.publisher.Publish(Event.EXIT_BED)
                    self.StartCheckBed()
                    self.nextZone.SetActive()
                    break
                else:
                    if time.time() - self.start_time > self.dormant_time:
                        self.ToggleLight("OFF")
                        self.nextZone.ToggleLight("OFF")
                    time.sleep(0.1)
            else:
                self.start_time = time.time()
                self.ToggleLight("ON")
                self.nextZone.ToggleLight("ON")
                time.sleep(0.1)


        

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
            if(self.IsOccupied()):
                self.SetActive()
            else:
                time.sleep(0.1)
        print(f"Bed: I no longer checkBed. user in bed: {self.userInBed}, systemIsActive: {self.systemIsActive}")

    
