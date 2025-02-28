import paho.mqtt.client as mqtt
import uuid
import command
import subprocess
import sys
import pygame

# the # wildcard means we subscribe to all subtopics of IDD
topic = 'IDD/party/#'

# some other examples
# topic = 'IDD/a/fun/topic'

#this is the callback that gets called once we connect to the broker.
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
	print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
	# you can filter by topics
	if msg.payload.decode('UTF-8') == 'child':
            subprocess.run(['sh', './child.sh'])
	if msg.payload.decode('UTF-8') == 'dance':
            pygame.mixer.init()
            pygame.mixer.music.load("song.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue


# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

# this is blocking. to see other ways of dealing with the loop
#  https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#network-loop
client.loop_forever()
