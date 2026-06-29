import time
import threading
from Enums.toggle import*

class Zone:
    def __init__(self, sensorReader = None,
                lightWriter = None,
                prevZone = None,
                nextZone = None):
        self.sensorReader = sensorReader
        self.lightWriter = lightWriter
        self.prevZone = prevZone
        self.nextZone = nextZone
        self.userInBed = True
        self.systemIsActive = True


    def ShutDown(self):
        print("Zone: The zone is shutting down")
        self.systemIsActive = False
        self.lightWriter.ShutDown()
        self.sensorReader.ShutDown()

    # Returns true if the sensor sees a person in the zone
    def IsOccupied(self):
        return self.sensorReader.isOccupied()

    # Sets the light to ON or OFF
    def ToggleLight(self, value):
        self.lightWriter.SetLight(value)

    def WhileActive(self): 
        while (not self.userInBed and self.systemIsActive):
            # If movement is seen in the next zone, and no movement is seen
            # in the current zone, the next zone is set as the active zone
            if (not self.IsOccupied() and self.nextZone.IsOccupied()):
                self.ToggleLight(Toggle.OFF)
                self.nextZone.SetActive()
                return
            # If movement is seen in the current zone, we stay here, and keep
            # the light on
            else:
                self.ToggleLight(Toggle.ON)
                self.nextZone.ToggleLight(Toggle.ON)
                time.sleep(0.1)
        self.ToggleLight(Toggle.OFF)
        self.nextZone.ToggleLight(Toggle.OFF)

    # Starts WhileActive as a thread
    def StartWhileActive(self):
        thread = threading.Thread(
            target = self.WhileActive,
            daemon = True
        )
        thread.start()

    # Function called when a zone becomes active
    def SetActive(self):
        self.StartWhileActive()
    
    

