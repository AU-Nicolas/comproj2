from time import sleep
import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("zigbee2mqtt/zone_1")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    payload_str = msg.payload.decode("utf-8")
    
    data = json.loads(payload_str)
    
    illuminance = data.get("illuminance")
    linkquality = data.get("linkquality")
    occupancy = data.get("occupancy")
    
    if (occupancy):
        client.publish("detection", "there is a human")
    else:
        client.publish("detection", "there is not a human")
    
    print("god message")
    
    
def on_publish(client, userdata, message_id):
    print(f"message with ID {message_id} published")

client = mqtt.Client()
# Client callback that is called when the client successfully connects to the broker.
client.on_connect = on_connect
# Client callback that is called when a message within the subscribed topics is published.
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
client.loop_forever()
