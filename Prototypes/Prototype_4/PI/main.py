from importer import*
from game_loop import*
from Data.light_writer import*
from Data.sensor_reader import*
from Business.toilet import*
from Business.bed import*
from Business.zone import*
from Business.manager import Manager
from Business.logging_service import LoggingService
from Data.data_sender import DataSender
from Business.scheduler import*

# Importing data
importer = Importer()
importer.importData("/home/lightway/Desktop/comproj2/Prototypes/Prototype_4/PI/game_map.json")

# Creating an instance of the game
game = GameLoop()

# Giving the walls to the game
game.walls = importer.walls

# Creating the manager
manager = Manager()

# Creating object for sending data to server
dataSender = DataSender("localhost")

# Creating the logging service
logger = LoggingService(dataSender)

# Extracting and setting up the bed
bed_zone = importer.zones[1]
game.sensors.append(bed_zone.sensor)
game.lights.extend(bed_zone.lights)

lightWriter = LightWriter(bed_zone.lights)
sensorReader = SensorReader(bed_zone.sensor)
bed = Bed(sensorReader, lightWriter)

# Giving the bed to the manager
manager.bed = bed

# The logger and manager subscribe to the bed
bed.publisher.Subscribe(logger)
bed.publisher.Subscribe(manager)

prevZone = bed
manager.zones.append(bed)

# Iterating over all normal zones
index = 2
while index+1 in importer.zones:
    # Retriving the current zone
    zone = importer.zones[index]
    
    # Adding game objects to the game
    game.sensors.append(zone.sensor)
    game.lights.extend(zone.lights)

    # Setting up data layer
    lightWriter = LightWriter(zone.lights)
    sensorReader = SensorReader(zone.sensor)

    # Setting up business layer
    zone = Zone(sensorReader, lightWriter)
    zone.prevZone = prevZone
    prevZone.nextZone = zone
    manager.zones.append(zone)
    prevZone = zone

    index += 1

bed.prevZone = bed.nextZone

# Setting up the toilet
toilet_zone = importer.zones[index]

game.sensors.append(toilet_zone.sensor)
game.lights.extend(toilet_zone.lights)

lightWriter = LightWriter(toilet_zone.lights)
sensorReader = SensorReader(toilet_zone.sensor)
toilet = Toilet(sensorReader, lightWriter, prevZone, prevZone)
prevZone.nextZone = toilet
manager.zones.append(toilet)

# The logger and manager subscribe to the toilet
toilet.publisher.Subscribe(logger)
toilet.publisher.Subscribe(manager)

# Creating the scheduler for stopping the program
scheduler = Scheduler(TimeStamp(12,30,30), manager, logger)
scheduler.StartSystem()
game.run()

