#%%
from pymongo import MongoClient
import configparser
import pandas as pd

class SensorFront():

    def __init__(self, nodes):
        """Sets up configuration for mongoDB"""
        config = configparser.ConfigParser()
        config.read('mongo.conf')
        self.username = config['conf']['username']
        self.password = config['conf']['password']
        self.hostname = config['conf']['hostname']
        self.port = config['conf']['port']
        self.db = config['conf']['db']

        self.nodes = nodes

    def get_all(self, node_id, n):
        """Get all values from database"""
        with MongoClient('mongodb://{}:{}@{}:{}/{}'.
                         format(self.username, self.password, self.hostname, self.port, self.db)) as client:
            values = [value for value in client['sensors'][node_id].find()]

        return values

    def get_n_latest(self, node_id, n):
        """Gets [n] latest values from [node_id]"""
        with MongoClient('mongodb://{}:{}@{}:{}/{}'.
                         format(self.username, self.password, self.hostname, self.port, self.db)) as client:
            values = [value for value in client['sensors'][node_id].find().sort('{$natural: -1}').limit(n)]

        return values

    def combine(self, n):
        """Combines [n] entries from all nodes into a dataframe"""
        temp = []
        for node in self.nodes:
            df = pd.DataFrame(self.get_n_latest(node, n))
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df['node'] = node
            temp.append(df)

        df = pd.concat([df for df in temp])

        return df




if __name__ == '__main__':
    sf = SensorFront(['node0', 'node1', 'node2', 'node3'])
#    ll=sf.get_latest('node0')
#    ll=sf.get_ll('node0', 7)

    df = sf.combine(10)



#%%
df.groupby('node')['humidity'].plot()


#%%

#%%

