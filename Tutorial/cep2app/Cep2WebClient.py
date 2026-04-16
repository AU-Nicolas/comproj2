import json
from dataclasses import dataclass
from typing import Any
import paho.mqtt.client as mqtt


@dataclass
class Cep2WebDeviceEvent:
    """ Represents a device event that is sent to the remote web service.
    """
    device_id: str
    device_type: str
    measurement: Any

    def to_json(self) -> str:
        """ Serializes the object to a JSON string.

        Returns:
            str: the event in JSON format
        """
        # The dumps() function serializes an object to a JSON string. In this case, it serializes a
        # dictionary.
        return json.dumps({"deviceId": self.device_id,
                           "deviceType": self.device_type,
                           "measurement": self.measurement})


class Cep2WebClient:
    def __init__(self, ip):
        self.client = mqtt.Client()
        self.client.connect(ip, 1883, 60)


    def send_event(self, event):
        self.client.publish("test", f"Sensor is occupied: {event}")
        
