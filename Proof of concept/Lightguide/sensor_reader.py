import paho.mqtt.client as mqtt
from time import sleep
import threading
import json

class SensorReader:
    def __init__(self, device_id, dormantTime = 4):
        self.cur_message_id = 0
        self.occupied = False
        self.dormantTime = dormantTime
        self.device_id = device_id

        # Ensuring that no no two threads can alter the same variables simultaneously
        self.lock = threading.Lock()
        # Timer meant for tracking dormant time
        self.timer = None
        
        # Setting up the client
        self.client = mqtt.Client()
        self.client.on_message = self.onMessage
        self.client.on_connect = self.onConnect
        self.client.connect("localhost", 1883, 60)
        
        self.client.loop_start()

    # When a message is received
    def onMessage(self, client, userdata, message):
        print("SensorReader: I receive a message")
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
            # If a timer already exists, it is cancelled
            if self.timer:
                self.timer.cancel()
            self.timer = threading.Timer(
                interval=self.dormantTime,
                function=self.SetOccupancyAsFalse
            )
            self.timer.start()
    
    # When connecting to the mqtt broker
    def onConnect(self, client, userdata, flags, rc):
        client.subscribe(f"zigbee2mqtt/{self.device_id}")
            
    # Will wait for timeDormant time. If no new thread has been started,
    # occupied will be set to false
    def SetOccupancyAsFalse(self):
        my_message_id = self.cur_message_id
        sleep(self.dormantTime)
        if(my_message_id == self.cur_message_id):
            self.occupied = False


    def isOccupied(self):
        return self.occupied