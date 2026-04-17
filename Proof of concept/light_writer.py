import paho.mqtt.client as mqtt
import json

class LightWriter:
    def __init__(self, device_id):
        self.device_id = device_id
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883, 60)


    def setLight(self, value):
        self.client.publish(topic=f"zigbee2mqtt/{self.device_id}/set",
                              payload=json.dumps({"state": f"{value}"}))