import networkx as nx
import json
import logging
import struct
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
# importing matplotlib.pyplot
import matplotlib.pyplot as plt
import os
import saturn_reader

mongo_pwd = os.environ['MONGO_PWD']
mongo_user = os.environ['MONGO_USER']


def convert_to_graph(net, xy):
    try:
        G = nx.Graph()
        for node in net.get('nodes', []):
            G.add_node(node['id'], num_links=node['num_links'], type=node['type'])
        for link in net.get('links', []):
            G.add_edge(link['from'],
                    link['to'],
                    id=link['to'],
                    num_lanes=link['num_lanes'],
                    travel_time=link['net_speed'],
                    distance=link['distance'],
                    turns=link['turns'])
        return G
    except Exception as e:
        logging.error(f"Error in converting data to graph: {e}")
        return None

def write_to_mongo(G, collection):
    try:
        # Convert graph to JSON-compatible dict
        data = nx.node_link_data(G)
        # Write data to MongoDB
        collection.insert_one(data)
    except Exception as e:
        logging.error(f"Error in writing data to MongoDB: {e}")

def read_from_mongo(collection):
    try:
        # Read data from MongoDB
        cursor = collection.find({})
        data = [json.loads(dumps(doc)) for doc in cursor]
        # Convert data back into a graph
        G = nx.node_link_graph(data[0])  # Assuming you only have one document in the collection
        return G
    except Exception as e:
        logging.error(f"Error in reading data from MongoDB: {e}")
        return None

def write_to_file(json_file):
    try:
        with open('output.json', 'w') as f:
            json.dump(json_file, f)
    except Exception as e:
        logging.error(f"Error in writing data to file: {e}")



def main():
  # Load your data here
  xy = saturn_reader.read_coordinate_file('saturn2.555')
  net = saturn_reader.read_saturn_111('saturn2.111', xy)
  
  write_to_file(net)
  #print(data2)
  # Convert data to a graph
  G = convert_to_graph(net, xy)

  uri = "mongodb+srv://" + mongo_user + ":" + mongo_pwd + "@cluster0.bg2ernm.mongodb.net/crmdb?retryWrites=true&w=majority"
  # Connect to MongoDB Atlas
  client = MongoClient(uri, server_api=ServerApi('1'))
  db = client['Cluster0']  # Use your database name
  collection = db['saturn']  # Use your collection name
  # Write graph to MongoDB
  write_to_mongo(G, collection)
  # Read graph from MongoDB
  #G2 = read_from_mongo(collection)
  #print(G2.nodes(data=True))
  #print(G2.edges(data=True))

  # Send a ping to confirm a successful connection
  #try:
  #  client.admin.command('ping')
  #  print("Pinged your deployment. You successfully connected to MongoDB!")
  #except Exception as e:
  #  print(e)

  nx.draw(G, with_labels=True)
  plt.savefig("filename.png")
  print('Done')

if __name__ == '__main__':
  main()
