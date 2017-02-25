# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from pytg import Telegram
from pytg.receiver import Receiver
from pytg.sender import Sender
import giphypop
g = giphypop.Giphy()
receiver = Receiver(host="localhost", port=4458)
sender = Sender(host="localhost", port=4458)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/opentrigger/signals/release")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("I GOT IT")
    print(msg.topic+" "+str(msg.payload))
    sender.send_msg("@Tanya_San", g.search('piglets').decode("utf-8"))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.188.38", 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
