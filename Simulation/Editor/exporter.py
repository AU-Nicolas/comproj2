from walls import*
from zones import*
import json

class Exporter:
    def __init__(self, zones, walls):
        self.zones = zones
        self.walls = walls
    
    def export(self, filename):
        # Data to be exported
        data = []
        # First all registered zones are added
        zone_id = 1
        for zone in self.zones.zones:
            # Adding the given sensor for the zone
            sensor = zone.sensor
            data.append({
                "type": "sensor",
                "zone": zone_id,
                "p0": sensor[0],
                "p1": sensor[1]
                })
            # Adding all the lights for the zone
            for light in zone.lights:
                data.append({
                    "type": "light",
                    "zone": zone_id,
                    "p0": light[0],
                    "p1": light[1]
                })
            zone_id += 1

        # Adding all the walls
        for wall in self.walls.objects:
            data.append({
                "type": "wall",
                "p0": wall[0],
                "p1": wall[1]
            })

        # Data is being exported
        with open(filename, "w") as f:
            json.dump(data, f)            

