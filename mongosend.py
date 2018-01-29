# %% Sensor network based on mongoDB
import configparser
from pymongo import MongoClient
import datetime
import Adafruit_DHT
import os

class SensorNode():

    def __init__(self, node_id):
        config = configparser.ConfigParser()
        config.read('mongo.conf')
        self.node_id = node_id
        self.username = config['conf']['username']
        self.password = config['conf']['password']
        self.hostname = config['conf']['hostname']
        self.port = config['conf']['port']
        self.db = config['conf']['db']

    def send_data(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        data = {'timestamp': datetime.datetime.now().timestamp(), 'humidity' : self.humidity, 'temperature' : self.temperature}

        with MongoClient('mongodb://{}:{}@{}:{}/{}'.
                         format(self.username, self.password, self.hostname, self.port, self.db)) as client:
            client['sensors'][self.node_id].insert_one(data)

if __name__ == '__main__':
    # Get device hostname for collection name
    hostname = os.popen('hostname').read().strip('\n')

    # Create SensorNode object with device hostname
    sn = SensorNode(node_id = hostname)

    # Take measurement and send to database
    sn.send_data()

