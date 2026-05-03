import paho.mqtt.client as mqtt
import json
from Business.db_updater import DBUpdater


class DataRetriever:
    def __init__(self,
                 handleMessageData,
                ip = "10.73.247.211", 
                topic = "toilet_info", 
                ack_topic = "toilet_info_ack"):
        
        # Function that decides what happens to data from a message
        self.handleMessageData = handleMessageData

        # MQTT topic for receiving data from the PI
        self.topic = topic
        # MQTT topic for sending acknowledgement to the PI
        self.ack_topic = ack_topic

        # Creating mqtt client
        self.client = mqtt.Client()
        self.client.on_connect = self.OnConnect
        self.client.on_message = self.OnMessage
        self.client.connect(ip, 1883, 60)

    # When a message is received, we add it to the database, and send
    # an acknowledgemessage back
    def OnMessage(self, client, userdata, message):
        # Getting the start time from the message
        try:
            data = json.loads(message.payload.decode())
            time_id = data["start"]

        # If there was an issue reading the message, we do nothing
        except (KeyError, json.JSONDecodeError):
            print("DataRetriever: We got a MQTT message error!")
            return
        
        # Sending an acknowledgement to the PI
        ack_message = json.dumps({"time_id": time_id})
        self.client.publish(self.ack_topic, ack_message)

        # Updating the database
        self.handleMessageData(data)

    # When connecting to the broker, we subscribe to the given topic
    def OnConnect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)
    
    def Loop(self):
        self.client.loop_forever()


