import paho.mqtt.client as mqtt
from pytg import Telegram
tg = Telegram(
    telegram="/home/pi/tg/bin/telegram-cli",
    pubkey_file="/home/pi/tg/server.pub")
receiver = tg.receiver
sender = tg.sender

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
    sender.send_msg("ramonmartin", "Hello World!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.188.38", 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
