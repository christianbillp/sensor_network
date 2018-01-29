#%%
from pymongo import MongoClient
import configparser
import pandas as pd
from datetime import datetime
from bokeh.plotting import figure, output_file, save
from bokeh.models import Range1d, LinearAxis
from bokeh.layouts import gridplot

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

    def get_all(self, node_id):
        """Get all values from database"""
        with MongoClient('mongodb://{}:{}@{}:{}/{}'.
                         format(self.username, self.password, self.hostname, self.port, self.db)) as client:
            values = [value for value in client['sensors'][node_id].find()]
        df = pd.DataFrame(values)
        df['timestamp'] = df['timestamp'].apply(datetime.fromtimestamp)
        df['node'] = node_id

        return df

    def get_n_latest(self, node_id, n):
        """Gets [n] latest values from [node_id]"""
        with MongoClient('mongodb://{}:{}@{}:{}/{}'.
                         format(self.username, self.password, self.hostname, self.port, self.db)) as client:
            values = [value for value in client['sensors'][node_id].find().sort('timestamp', -1).limit(n)]

        df = pd.DataFrame(values)
        df['timestamp'] = df['timestamp'].apply(datetime.fromtimestamp)

        return df

    def get_dataframe(self, n):
        """Combines [n] entries from all nodes into a dataframe"""
        temp = []
        for node in self.nodes.keys():
            df = pd.DataFrame(self.get_n_latest(node, n))
            df['node'] = node
            temp.append(df)

        df = pd.concat([df for df in temp])

        return df

    def generate_html(self, n):
        """Generates html for info page"""
        pl = {}
        for node in self.nodes.keys():
            output_file("graphs.html")
            df = sf.get_n_latest(node, n)

            pl[node] = figure(x_axis_type='datetime', plot_width=800, plot_height=350,
                       title="{} - {}".format(node, self.nodes[node]), toolbar_location="above",
                       tools = "pan, wheel_zoom, box_zoom, reset",
                       y_range=Range1d(16, 30))
            pl[node].line(df['timestamp'], df['temperature'], color='blue')
            pl[node].yaxis.axis_label = 'Degrees C'
            pl[node].extra_y_ranges = {"humidity": Range1d(start=20, end=60)}
            pl[node].add_layout(LinearAxis(y_range_name="humidity", axis_label='% humidity'), 'right')
            pl[node].line(df['timestamp'], df['humidity'], y_range_name="humidity", color='green')

        save(gridplot([[pl[node]] for node in self.nodes.keys()]))

        with open('info.html', 'w') as f:
            graphs = open('graphs.html', 'r').read()
#            f.write("""<?php include 'protect.php';?>""")
            f.write('<h1>Temperature and Humidity plots</h1>')
            f.write(graphs)


if __name__ == '__main__':
    # Construct SensorFront object from dictionary
    sf = SensorFront({'node0' : 'bedroom', 'node1' : 'kitchen', 'node2' : 'living room', 'node3' : 'office', })

    # Get all values from node0
    node0_all = sf.get_all('node0')

    # Get 100 values from node0
    latest100 = sf.get_n_latest('node1', 100)

    # Get latest value from database
    latest = sf.get_dataframe(1)
    print(latest)

    # Create a dataframe from the latest 500 values
    df = sf.get_dataframe(1000)

    # Create html page for visualization
    sf.generate_html(3000)

#%% End of File

