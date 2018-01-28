import paho.mqtt.client as mqtt
import Adafruit_DHT
import os
import RPi.GPIO as GPIO

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(int(rc)))
    print("Connected to: {}".format(server_address))


def on_message(client, userdata, msg):
    print("[{}]: {}".format(msg.topic, str(msg.payload, "utf-8")))

server_address = 'SERVER_ADDRESS'
nodes = 'LIST OF NODES [name, name, name...]'
sensor = Adafruit_DHT.DHT22
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host=server_address, port=1883, keepalive=60)


try:
    myname = os.popen('hostname').read().strip('\n')
    output = 0
    node1values = "{:.1f}\t{:.1f}\t{}\t{}".format(temperature, humidity, output, GPIO.input(17))
    client.publish(myname, node1values)
finally:
    client.disconnect()
