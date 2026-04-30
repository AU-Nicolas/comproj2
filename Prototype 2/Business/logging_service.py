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
        
        toilet_events = []
        startTime, endTime = None

        for event in self.events:
            if event.type == Event.EXIT_BED:
                # Checking that we only are exiting the bed in the beginning of the events
                if event.time != self.events[0].time:
                    print("Unexpected placement of exit bed event")
                    break
                # Registering the beginning of the actions
                startTime = event.time
            
            elif event.type == Event.ENTER_BED:
                # Checking that this is the last stored event
                if event.time != self.events[-1].time:
                    print("Unexpected placement of enter bed event")
                    break
                # Registering the end of the actions
                endTime = event.time

            else:
                toilet_events.append(event)
            
        tot_toilet_time = (0,0)
        # Checking that there is an even amount of toilet events (as expected)
        if len(toilet_events % 2 == 0):
            expected_event_type = Event.ENTER_TOILET
            # Looping through all toilet events to calculate accumulated toilet time
            last_time = (0,0)
            for event in toilet_events:
                if(event.type != expected_event_type):
                    tot_toilet_time = (0,0)
                    print("Unexpected placement of toilet event")
                    break
                if last_time == (0,0):
                    last_time = (event.time.minute, event.time.second)
                else:
                    


                



        data["start"] = startTime.strftime("%Y-%m-%d %H:%M:%S")
                
                

        # Sending the message to the datasender
        message = json.dumps(data)
        self.dataSender.SendMessage(message)

            

