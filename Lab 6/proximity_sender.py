import time
import board
import busio
import adafruit_mpr121

import paho.mqtt.client as mqtt
import uuid

from adafruit_apds9960.apds9960 import APDS9960

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/your/topic/here'

i2c = busio.I2C(board.SCL, board.SDA)
apds = APDS9960(i2c)
apds.enable_proximity = True

while True:
    for i in range(12):
        val = "proximity: " + str(apds.proximity)
        print(val)
        client.publish(topic, val)
    time.sleep(0.25)
