from light_writer import*
from sensor_reader import*
from time import sleep


sensor1 = SensorReader("sensor_1")
light1 = LightWriter("light_1")

while(True):
    if(sensor1.isOccupied()):
        light1.setLight("ON")
    else:
        light1.setLight("OFF")
    sleep(1)
