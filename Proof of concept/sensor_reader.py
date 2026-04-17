import paho.mqtt.client as mqtt
from time import sleep

class SensorReader:
    def __init__(self, device_id, dormantTime = 4):
        self.cur_message_id = 0
        self.occupied = False
        self.dormantTime = dormantTime

        # Setting up the client
        self.client = mqtt.Client()
        self.client.subscribe(f"zigbee2mqtt/{device_id}")
        self.client.on_message = self.onMessage
        self.client.connect("localhost", 1883, 60)
        self.client.loop_forever()

    def onMessage(self, client, userdata, message):
        # Checking if message has property occupancy
        try:
            occupancy = message.event["occupancy"]
        except KeyError:
            pass
        else:
            # If the sensor detects motion, we set occupied to true
            if(occupancy):
                self.occupied = True
            # If a false reading is detected we wait for dormantTime seconds.
            # If no new reading is produced, we set occupied to false
            else:
                self.cur_message_id += 1
                my_message_id = self.cur_message_id
                sleep(self.dormantTime)
                if(my_message_id == self.cur_message_id):
                    self.occupied = False



    def isOccupied(self):
        return self.occupied