import datetime as dt
from time import sleep
import threading

class TimeStamp:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

class Scheduler:
    def __init__(self, endTime,
                manager = None,
                loggingService = None):
        self.endTime = None
        self.SetEndTime(endTime)
        self.manager = manager
        self.loggingService = loggingService

    # Setting the time for when the scheduler should shut the system down
    def SetEndTime(self, endTime):
        # Setting the correct day for the endtime by setting it to today
        now = dt.datetime.now()
        self.endTime = now

        # Converting the input into a datetime time
        self.endTime = self.endTime.replace(hour=endTime.hour,
                             minute=endTime.minute,
                             second=endTime.second)

        # If the given endtime has happened today, we set the endtime to tomorrow
        if(self.endTime < now):
            self.endTime += dt.timedelta(seconds=86400)

    def StartSystem(self):
        # Starting up the manager and logging service
        self.manager.StartUp()
        self.loggingService.StartUp()

        # Starting CheckTime as a thread
        thread = threading.Thread(
            target=self.CheckTime,
            daemon=True
        )
        thread.start()


    def ShutDownSystem(self):
        self.manager.ShutDown()
        self.loggingService.ShutDown()
        
    def CheckTime(self):
        while(True):
            # If we have exceeded the end time, the system shuts down
            if dt.datetime.now() > self.endTime:
                print("Scheduler: I shot everything down")
                self.ShutDownSystem()
                break
            else:
                sleep(1)

            
            
    
