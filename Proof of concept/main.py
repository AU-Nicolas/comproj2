from light_writer import*
from sensor_reader import*
from time import sleep
import paho.mqtt.client as mqtt


ip = "10.178.157.211"

# Creating sensor and light objects
sensor1 = SensorReader("sensor_1")
light1 = LightWriter("light_1")

# Creating mqtt publisher
client = mqtt.Client()
client.connect(ip, 1883, 60)
topic = "occupied"

occupied = False

while(True):
    if(sensor1.isOccupied()):
        if not occupied:
            client.publish("Sensor is occupied")
        occupied = True
        light1.setLight("ON")
    else:
        if occupied:
            client.publish("Sensor is not occupied")
        occupied = False
        light1.setLight("OFF")

    sleep(0.2)
