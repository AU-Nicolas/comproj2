from Enums.event import*
from datetime import datetime
import threading
import json
from Business.pubsub import Subscriber

class EventTime:
    def __init__(self, type, time):
        self.type = type
        self.time = time

# Inherits from subscriber - will subscribe to bed and toilet
class LoggingService(Subscriber):
    def __init__(self, dataSender):
        self.events = []
        self.lock = threading.Lock()
        self.dataSender = dataSender
    
    def ShutDown(self):
        self.dataSender.ShutDown()
    
    def StartUp(self):
        self.dataSender.StartUp()

    # What happens when a message is received from a publisher
    def Receive(self, event_type):
        print(f"LoggingService: I receive a publish: {event_type}")
        # Registering the given event
        event = EventTime(event_type, datetime.now())
        # Ensures that only one instance of register event is running
        with self.lock:
            self.events.append(event)
            # If the resident enters the bed, we flush all stored events
            if(event_type == Event.ENTER_BED):
                print("LoggingService: I really should run this, huh")
                self.FlushEvents()
    

    def FlushEvents(self):
        print("LoggingService: I start to flush events")
        # The data that will be sent
        data = {"start": "", 
                "total_time": 0,
                "completed": False,
                "to_toilet": 0,
                "on_toilet": 0,
                "to_bed": 0}
        
        # starttime, endtime = None
        
        # Checks if the first event is in fact exit bed
        if (self.events[0].type == Event.EXIT_BED):
            # Registering the start time
            starttime = self.events[0].time
            data["start"] = starttime
            del self.events[0]
        # If not, we return
        else:
            self.events = []
            print("Error: First event is not EXIT_BED")
            return
        
        # Checks if the last event is in fact exit bed
        if (self.events[-1].type == Event.ENTER_BED):
            # Registering the end time and calculating total time
            endtime = self.events[-1].time
            data["total_time"] = (endtime - starttime).seconds
            del self.events[-1]
        # If not, we return
        else:
            self.events = []
            print("Error: Last event is not ENTER_BED")
            return
        
        # If there are no more events, we return
        if (len(self.events) == 0):
            self.SendData(data)
            return
        
        # Checking that we first enter the toilet
        if (self.events[0].type == Event.ENTER_TOILET):
            # Registering time to toilet
            data["to_toilet"] = (self.events[0].time - starttime).seconds
        else:
            # Returning if the data was weird
            self.SendData(data)
            print("Error: weird toilet behavior - missing entry")
            return
        
        # Checking that the toilet is left
        if (self.events[-1].type == Event.EXIT_TOILET):
            # Registering time to the bed
            data["to_bed"] = (endtime - self.events[-1].time).seconds
        else:
            # Returning if the data was weird
            self.SendData(data)
            print("Error: weird toilet behavior - missing exit")
            return
        
        # Checking that we enter and exit the toilet the same number of times
        if (len(self.events) % 2 != 0):
            self.SendData(data)
            return
        
        # Registering the total time spent in the toilet
        expected_event = Event.ENTER_TOILET
        on_toilet = 0
        enter_time = None

        for event in self.events:
            # If we get an unexpected event, we return
            if (expected_event != event.type):
                self.SendData(data)
                return
            
            if (event.type == Event.ENTER_TOILET):
                expected_event = Event.EXIT_TOILET
                enter_time = event.time
            
            elif (event.type == Event.EXIT_TOILET):
                expected_event = Event.ENTER_TOILET
                on_toilet += (event.time - enter_time).seconds
            

        data["on_toilet"] = on_toilet
        # Registering the toilet visit as complete
        data["completed"] = True
        self.SendData(data)
        
    
    def SendData(self, data):
        # If the toilet visit wasn't complete, we include no data about the toilet time
        if (data["completed"] == False):
            data["on_toilet"] = 0
            data["to_toilet"] = 0
            data["to_bed"] = 0
        # Events is reset
        self.events = []
        # The data is sent to the datasender
        self.dataSender.AddMessage(data)