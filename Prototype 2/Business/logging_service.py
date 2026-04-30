from Enums.event import*
from datetime import datetime
import threading
import json

class EventTime:
    def __init__(self, type, time):
        self.type = type
        self.time = time

class LoggingService:
    def __init__(self, dataSender):
        self.events = []
        self.lock = threading.Lock()
        self.dataSender = dataSender
    
    def RegisterEvent(self, event_type):
        # Ensures that only one instance of register event is running
        with self.lock:
            # Registering the given event
            event = EventTime(event_type, datetime.now())
            self.events.append(event)
            # If the resident enters the bed, we flush all stored events
            if(event == Event.ENTER_BED):
                self.FlushEvents()
    

    def FlushEvents(self):
        # The data that will be sent
        data = {"start": "", 
                "total_time": (0,0),
                "completed": False,
                "to_toilet": (0,0),
                "on_toilet": (0,0),
                "to_bed": (0,0)}
        
        starttime, endtime = None
        
        if (self.events[0].type == Event.EXIT_BED):
            starttime = self.events[0].time
            data["start"] = starttime.strftime("%Y-%m-%d %H:%M:%S")
            del self.events[0]
        else:
            self.events = []
            print("Error: First event is not EXIT_BED")
            return
        
        if (self.events[-1].type == Event.ENTER_BED):
            endtime = self.events[-1].time
            delta = (endtime - starttime).seconds
            data["total_time"] = self.ConvertTime(delta)
            del self.events[-1]
        else:
            self.events = []
            print("Error: Last event is not ENTER_BED")
            return
    
        if (len(self.events) == 0):
            self.SendData(data)
            return
        
        if (self.events[0].type == Event.ENTER_TOILET):
            delta = (self.events[0].time - starttime).seconds
            data["to_toilet"] = self.ConvertTime(delta)
        else:
            self.SendData(data)
            print("Error: weird toilet behavior - missing entry")
            return
        
        if (self.events[-1].type == Event.EXIT_TOILET):
            delta = (endtime - self.events[-1].time).seconds
            data["to_bed"] = self.ConvertTime(delta)
        else:
            self.SendData(data)
            print("Error: weird toilet behavior - missing exit")
            return
        
        if (len(self.events) % 2 != 0):
            self.SendData(data)
            return
        
        expected_event = Event.ENTER_TOILET
        on_toilet = 0
        enter_time = None

        for event in self.events:
            if (expected_event != event.type):
                self.SendData(data)
                return
            
            if (event.type == Event.ENTER_TOILET):
                expected_event = Event.EXIT_TOILET
                enter_time = event.time
            
            elif (event.type == Event.EXIT_TOILET):
                expected_event = Event.ENTER_TOILET
                on_toilet += (event.time - enter_time).seconds
            

        data["on_toilet"] = self.ConvertTime(on_toilet)
        data["completed"] = True
        self.SendData(data)
        

    def ConvertTime(self, time_seconds):
        minutes = time_seconds // 60
        seconds = time_seconds % 60
        return (minutes, seconds)
    
    def SendData(self, data):
        if (data["completed"] == False):
            data["on_toilet"], data["to_toilet"], data["to_bed"] = (0,0)
        
        self.events = []
        # Sending the message to the datasender
        message = json.dumps(data)
        self.dataSender.AddMessage(message)

            

