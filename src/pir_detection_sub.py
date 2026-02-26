from time import sleep
import paho.mqtt.client as mqtt
import json

# Når lokale klient forbinder til localhost
def on_connect_local(client, userdata, flags, rc):
    print("Connected local with result code "+str(rc))
    # Lokale klient subscriber til sensor
    client.subscribe("zigbee2mqtt/zone_1")

# Når offentlige klient forbinder til IP
def on_connect_public(client, userdata, flags, rc):
    print("Connected public with result code "+str(rc))

# Når lokale klient modtager besked fra sensor
def on_sensor_message(client, userdata, msg):
    # Konverterer besked fra json til dictionary
    payload_str = msg.payload.decode("utf-8")
    data = json.loads(payload_str)
    
    # Data extractes fra dictionary
    illuminance = data.get("illuminance")
    linkquality = data.get("linkquality")
    occupancy = data.get("occupancy")
    
    # Public klient sender besked over IP baseret på data fra sensor
    if (occupancy):
        client_public.publish("detection", "there is a human")
    else:
        client_public.publish("detection", "there is not a human")
    
    print("god message")
    
    
# Lokale klient laves
client_local = mqtt.Client()
# Connect-funktion sættes
client_local.on_connect = on_connect_local
# On_message funktion sættes
client_local.on_message = on_sensor_message



# Public client laves
client_public = mqtt.Client()
# Connect-funktion sættes
client_public.on_connect = on_connect_public

# Klienter forbinder til IP-adresser
client_local.connect("localhost", 1883, 60)
client_public.connect("10.112.196.211", 1883, 60)


# Lokale klient lytter konstant
client_local.loop_forever()
