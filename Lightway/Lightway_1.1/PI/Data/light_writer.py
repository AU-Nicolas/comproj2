import paho.mqtt.client as mqtt
from Enums.toggle import Toggle
import threading
import json


class LightWriter:
    def __init__(self, device_id):
        self.device_id = device_id
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883, 60)
        # What is the belief of the current light state?
        self.settingToValue = Toggle.ON
        # Setting the light to off initially
        self.SetLight(Toggle.OFF)
        self.client.loop_start()

    def SetLight(self, value):
        # Ensuring only one instance can run
        with self.lock:
            # If we already are setting to the current value, we abort
            if(value == self.settingToValue):
                return
            
            # Updating the value we are setting to
            self.settingToValue = value

            # If something is currently setting, we cancel that proces
            if self.timer:
                self.timer.cancel()
            
            # We will now change the light in self.changeTime time
            self.timer = threading.Timer(
                interval=self.changeTime,
                function=self.ChangeLight,
                args=(value,)
            )
            self.timer.start()

    def ChangeLight(self, value):
        with self.lock:
            # Returns if we somehow are setting to some value different than
            # the most recently desired one
            if value != self.settingToValue:
                return
            
            # The light is changed
            self.client.publish(topic=f"zigbee2mqtt/{self.device_id}/set",
                                payload=json.dumps({"state": f"{value}"}))

    def ShutDown(self):
        print("LightWriter: Is shutting down")
        self.client.disconnect()
        self.client.loop_stop()