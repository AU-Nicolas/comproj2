from importer import*
from game_loop import*
from Business.light_writer import*
from Business.sensor_reader import*
from Business.zone_manager import*

# Importing data
importer = Importer()
importer.importData("game_map.json")

# Creating an instance of the game
game = GameLoop()

# Giving the walls to the game
game.walls = importer.walls
zoneManagers = []

# Iterating over all valid zones
index = 1
while True:
    # We exit of the importer no longer contains any valid zones
    if index not in importer.zones:
        break

    # Retriving the current zone
    zone = importer.zones[index]
    
    # Adding game objects to the game
    game.sensors.append(zone.sensor)
    game.lights.extend(zone.lights)

    # Setting up data layer
    lightWriter = LightWriter(zone.lights)
    sensorReader = SensorReader(zone.sensor)

    # Setting up business layer
    zoneManager = ZoneManager(lightWriter, sensorReader)
    zoneManagers.append(zoneManager)

    index += 1

for zoneManager in zoneManagers:
    zoneManager.start()

game.run()

for zoneManager in zoneManagers:
    zoneManager.stop()