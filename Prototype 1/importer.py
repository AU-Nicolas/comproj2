from Objects.zone import*
from Objects.sensor import*
from Objects.light import*
from Objects.wall import*


import json

class Importer:
    def __init__(self):
        self.walls = []
        self.zones = {}
    
    def importData(self, filename):
        
        # Opening the file
        with open(filename, "r") as f:
            data = json.load(f)
        
        # Looping through all entries in the file
        for entry in data:
            type = entry["type"]

            # Converting to tuple from list
            p0 = tuple(entry["p0"])
            p1 = tuple(entry["p1"])

            if type == "wall":
                self.walls.append(Wall(p0,p1))
            
            # If the current object something in a zone
            else:
                zone_id = entry["zone"]
                if zone_id not in self.zones:
                    self.zones[zone_id] = Zone()
                # The current zone we are working with
                zone = self.zones[zone_id]
                
                if(type == "sensor" and zone.sensor == None):
                    zone.sensor = Sensor(p0,p1)
                
                elif(type == "light"):
                    zone.lights.append(Light(p0,p1))



                
