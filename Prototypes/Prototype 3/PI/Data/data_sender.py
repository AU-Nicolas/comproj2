import paho.mqtt.client as mqtt
from time import sleep
import threading
import json

class DataSender:
    def __init__(self, 
                ip, 
                topic = "toilet_info", 
                ack_topic = "toilet_info_ack"):
        
        
        # Dictionary of messages that must be sent to the server
        # The start time acts as the key
        self.messages = {}

        # MQTT topic for sending data to server
        self.topic = topic
        # MQTT topic for receiving acknowledgement from the server
        self.ack_topic = ack_topic

        # Creating mqtt client
        self.client = mqtt.Client()
        self.client.on_connect = self.OnConnect
        self.client.on_message = self.OnMessage
        self.client.connect(ip, 1883, 60)
        self.client.loop_start()
        
        # MQTT topic for sending data to server
        self.topic = topic
        # MQTT topic for receiving acknowledgement from the server
        self.ack_topic = ack_topic

        # Flag that signifies that data is currently being sent to server
        self.isSending = False
    
    # Function for adding message to message list
    def AddMessage(self, data):
        print("DataSender: I add a message to my message list")
        # Converting datetime to string for json formatting
        time_id = data["start"].strftime("%Y-%m-%d %H:%M:%S")
        data["start"] = time_id
        # Adding the message
        message = json.dumps(data)
        self.messages[time_id] = message
    
    # Function that enables the class to start sending data to the server
    def StartSending(self):
        print("DataSender: I should start sending messages")
        self.isSending = True
        thread = threading.Thread(
            target = self.SendData,
            daemon = True
        )
        thread.start()
    
    def StopSending(self):
        self.isSending = False

    # Tries to send data to the server every 10 seconds
    def SendData(self):
        while(self.isSending):
            for message in self.messages.values():
                print("DataSender: I sent a message!")
                self.client.publish(self.topic, message)
            sleep(10)
    
    # The client subscribes to the acknowledgement topic when connecting
    def OnConnect(self, client, userdata, flags, rc):
        client.subscribe(self.ack_topic)
    
    # When a message on the acknowledgement topic is received corresponding to some
    # message ID, that message is removed from the message list, such that it is no
    # longer sent over
    def OnMessage(self, client, userdata, message):
        # Checking if message has correct properties
        try:
            payload = json.loads(message.payload.decode())
            time_id = payload["time_id"]

        # If there was an issue reading the message, we do nothing
        except (KeyError, json.JSONDecodeError):
            print("DataSender: We got a MQTT message error!")
            return
        
        if time_id in self.messages:
            self.messages.pop(time_id)


    

