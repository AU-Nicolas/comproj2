from Data.light_writer import*
from Data.sensor_reader import*
from Business.toilet import*
from Business.bed import*
from Business.zone import*
from Business.manager import Manager
from Business.logging_service import LoggingService
from Data.data_sender import DataSender
from Business.scheduler import*
from datetime import datetime
from time import sleep

with open("/home/lightway/Desktop/comproj2/Lightway_1.0/PI/logfile.txt", "a") as f:
    f.write(f"I logged at {datetime.now()}\n")
    f.close()

# Creating the manager
manager = Manager()

# Creating object for sending data to server
dataSender = DataSender("localhost")

# Creating the logging service
logger = LoggingService(dataSender)



lightWriter = LightWriter("light_bed")
sensorReader = SensorReader("sensor_bed")
bed = Bed(sensorReader, lightWriter, dormant_time=4)

# Giving the bed to the manager
manager.bed = bed

# The logger and manager subscribe to the bed
bed.publisher.Subscribe(logger)
bed.publisher.Subscribe(manager)

prevZone = bed
manager.zones.append(bed)

# Iterating over all normal zones
for i in range(1,2):


    # Setting up data layer
    lightWriter = LightWriter(f"light_{i}")
    sensorReader = SensorReader(f"sensor_{i}")

    # Setting up business layer
    zone = Zone(sensorReader, lightWriter)
    zone.prevZone = prevZone
    prevZone.nextZone = zone
    manager.zones.append(zone)
    prevZone = zone

bed.prevZone = bed.nextZone



lightWriter = LightWriter("light_toilet")
sensorReader = SensorReader("sensor_toilet")
toilet = Toilet(sensorReader, lightWriter, prevZone, prevZone)
prevZone.nextZone = toilet
manager.zones.append(toilet)

# The logger and manager subscribe to the toilet
toilet.publisher.Subscribe(logger)
toilet.publisher.Subscribe(manager)

# Creating the scheduler for stopping the program
scheduler = Scheduler(TimeStamp(17,2), manager, logger)
scheduler.StartSystem()

while(scheduler.systemIsActive):
    sleep(1)

