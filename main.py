# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from pytg import Telegram
import json
import random
import os
import requests
import giphypop
g = giphypop.Giphy()

tg = Telegram(
    telegram="/home/pi/tg/bin/telegram-cli",
    pubkey_file="/home/pi/tg/bin/tg-server.pub")
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
    uuid = json.loads(msg.payload)['UniqueIdentifier']
    age = json.loads(msg.payload)['Age']
    with open("/var/www/reflexpress/public/config.json", "r") as content:
        config = json.loads(content)
        if uuid == config['uuid']:
            if int(age) > 500:
                search_term = random.choice(config['long'])
                gif = random.choice([x for x in g.search(search_term)])
                page = requests.get(gif.fixed_height.downsampled.url)
                with open("/tmp/temp.gif", "wb") as f:
                    f.write(page.content)
                sender.send_file(config['recipient'], u"/tmp/temp.gif")
                os.remove("/tmp/temp.gif")
            else:
                sender.send_msg(config['recipient'], random.choice(config['short']))
        else:
            sender.send_msg("Tanya_San", u"😜")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
