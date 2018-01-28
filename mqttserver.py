import pymysql.cursors
import paho.mqtt.client as mqtt
import datetime

connection = pymysql.connect(host='SERVERNAME',
                             user='USERNAME',
                             password='PASSWORD',
                             db='DATABASE',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def add_data(node, temperature, humidity, outputvalue, pir):
    with connection.cursor() as c:
        # c.execute("INSERT INTO {} VALUES (NULL, NOW(),{},{},{})".format(node, temperature, humidity, outputvalue))
        c.execute("INSERT INTO {} (ts, temperature, humidity, output, pir) VALUES (NOW(),{},{},{},{})"
                  .format(node, temperature, humidity, outputvalue, pir))

        connection.commit()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(int(rc)))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    message = msg.payload.decode('utf-8').split('\t')
    print("{}: [{}] - {}".format(datetime.datetime.now(), msg.topic, message))
    add_data(msg.topic, message[0], message[1], message[2], message[3])


print("System ready")
client = mqtt.Client()
client.on_message = on_message

# Needs MQTT server name
servername = "MQTT_SERVERNAME"

# Needs MQTT server port
client.connect(servername, "SERVERPORT", 60)
print("connected")

client.subscribe([('node0', 0),('node1', 1),('node2', 2),('node3', 2)])

try:
    while True:
        client.loop()
except IndexError:
    pass
finally:
    client.disconnect()
    print("Disconnected")
