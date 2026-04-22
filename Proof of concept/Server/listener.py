import paho.mqtt.client as mqtt
from time import sleep
import threading
import json
from datetime import datetime

class Listener:
    def __init__(self, dbManager,
                 ip = "10.178.157.211", 
                 topic = "occupancy"):
        # Databasemanager we write to
        self.dbManager = dbManager
        # MQTT topic
        self.topic = topic        
        
        # Setting up the client
        self.client = mqtt.Client()
        self.client.on_message = self.onMessage
        self.client.on_connect = self.onConnect
        self.client.connect(ip, 1883, 60)

    # When a message is received
    def onMessage(self, client, userdata, message):
        # Checking if message has correct properties
        try:
            payload = json.loads(message.payload.decode())
            occupancy = payload["occupied"]
            time_str = payload["time"]

        # If there was an issue reading the message, we do nothing
        except (KeyError, json.JSONDecodeError):
            print("We got a message error!!!")
            return
        
        # Converting time from string to datetime
        time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

        # Writing to the database
        self.dbManager.writeToDatabase(occupancy, time)
        
    
    # When connecting to the mqtt broker
    def onConnect(self, client, userdata, flags, rc):
       client.subscribe(self.topic)

    def loop(self):
        self.client.loop_forever()