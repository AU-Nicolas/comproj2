import time
import threading

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
        self.lightWriter.setLight(value)

    def CheckIfActive(self): 
        while (not self.userInBed and self.systemIsActive):
            if (not self.IsOccupied() and self.nextZone.IsOccupied()):
                self.ToggleLight("OFF")
                self.nextZone.SetActive()
                break
            else:
                time.sleep(0.1)
        self.ToggleLight("OFF")



    # Starts CheckIfActive as a thread
    def StartCheckIfActive(self):
        thread = threading.Thread(
            target = self.CheckIfActive,
            daemon = True
        )
        thread.start()

    # Function called when a zone becomes active
    def SetActive(self):
        self.ToggleLight("ON")
        self.nextZone.ToggleLight("ON")
        self.StartCheckIfActive()
    
    

