import paho.mqtt.client as mqtt
from time import sleep
import threading
import json

class SensorReader:
    def __init__(self, device_id, dormantTime = 4):
        self.cur_message_id = 0
        self.occupied = False
        self.dormantTime = dormantTime
        # Setting up the client
        self.client = mqtt.Client()
        self.client.on_message = self.onMessage
        self.client.connect("localhost", 1883, 60)
        self.client.subscribe(f"zigbee2mqtt/{device_id}")
        self.client.loop_start()

    def onMessage(self, client, userdata, message):
        # Checking if message has property occupancy
        try:
            payload = json.loads(message.payload.decode())
            occupancy = payload["occupancy"]
        except (KeyError, json.JSONDecodeError):
            return
        self.cur_message_id += 1
        # If the sensor detects motion, we set occupied to true
        if(occupancy):
            self.occupied = True
        # If a false reading is detected we start a set false thread
        else:
            thread = threading.Thread(
                target = self.setFalse,
                daemon = True
            )
            thread.start()
            
    # Will wait for timeDormant time. If no new thread has been started,
    # occupied will be set to false
    def setFalse(self):
        my_message_id = self.cur_message_id
        sleep(self.dormantTime)
        if(my_message_id == self.cur_message_id):
            self.occupied = False


    def isOccupied(self):
        return self.occupied