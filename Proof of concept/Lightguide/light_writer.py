import paho.mqtt.client as mqtt
import threading
import json
import time

class LightWriter:
    def __init__(self, device_id):
        self.device_id = device_id
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883, 60)

        # What is the belief of the current light state?
        self.lightStatus = "ON"
        # Do we have confirmation that the light has been changed?
        self.hasConfirmation = False
        # Current thread id - only one thread should run at a time
        self.threadID = 0
        # Setting the light to off initially
        self.setLight("OFF")

    def setLightThread(self, value, threadID):
        while not self.hasConfirmation and self.threadID == threadID:
            self.client.publish(topic=f"zigbee2mqtt/{self.device_id}/set",
                                payload=json.dumps({"state": f"{value}"}))
            time.sleep(1)
            

    def setLight(self, value):
        if(self.lightStatus != value):
            self.hasConfirmation = False
            # Incrementing the thread ID
            self.threadID += 1
            # Copying threadID as parameter
            threadID = self.threadID
            # Starting the thread
            thread = threading.Thread(
                target = self.setLightThread,
                args=(value, threadID),
                daemon = True
            )
            thread.start()
            self.lightStatus = value