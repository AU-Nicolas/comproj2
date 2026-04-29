from light_writer import*
from sensor_reader import*
from time import sleep
import paho.mqtt.client as mqtt
import json
from datetime import datetime


ip = "10.73.247.211"

# Creating sensor and light objects
sensor1 = SensorReader("sensor_1")
light1 = LightWriter("light_1")

# Creating mqtt publisher
client = mqtt.Client()
client.connect(ip, 1883, 60)
client.loop_start()
topic = "occupancy"

occupied = False

def publish_data(occupancy):
    time = datetime.now()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    data = {"occupied":occupancy, "time":time_str}
    json_data = json.dumps(data)
    client.publish(topic, json_data)

while(True):
    if(sensor1.isOccupied()):
        if not occupied:
            publish_data(True)
            print("I should publish occupied!")
        occupied = True
        light1.setLight("ON")
    else:
        if occupied:
            publish_data(False)
            print("I should publish not occupied!")
        occupied = False
        light1.setLight("OFF")

    sleep(0.2)
