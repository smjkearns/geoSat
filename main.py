import networkx as nx
import json
import struct
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
# importing matplotlib.pyplot
import matplotlib.pyplot as plt


def read_saturn_file(file_name):
  data = {'nodes': [], 'links': []}
  with open(file_name, 'r') as file:
    for line in file.readlines():
      if len(line) > 5:  # Skip blank lines
        if line[5] == " ":  # This line represents a node
          id = int(line[0:5])
          node = {
            'id': int(line[0:5]),
            'num_links': int(line[6:10]),
            'type': int(line[11:15])
          }
          data['nodes'].append(node)
        else:  # This line represents a link
          link = {
            #'id': int(line[0:10]),
            'from':
            int(line[5:10]),
            'to':
            id,
            'num_lanes':
            int(line[14]),
            'net_speed':
            int(line[15:20]),
            'distance':
            int(line[20:25]),
            'turns': [{
              'saturation_flow': int(line[25:30]),
              'priority_marker': line[30],
              #'modifier': int(line[46:50]),
              'first_lane': int(line[32]),
              'last_lane': int(line[34])
            }]
          }
          data['links'].append(link)
          #print(data)
  return data


def convert_to_graph(data):
  G = nx.Graph()
  for node in data['nodes']:
    G.add_node(node['id'], num_links=node['num_links'], type=node['type'])
  for link in data['links']:
    G.add_edge(link['from'],
               link['to'],
               id=link['to'],
               num_lanes=link['num_lanes'],
               travel_time=link['net_speed'],
               distance=link['distance'],
               turns=link['turns'])
  return G


def write_to_mongo(G, collection):
  # Convert graph to JSON-compatible dict
  data = nx.node_link_data(G)
  # Write data to MongoDB
  collection.insert_one(data)


def read_from_mongo(collection):
  # Read data from MongoDB
  cursor = collection.find({})
  data = [json.loads(dumps(doc)) for doc in cursor]
  # Convert data back into a graph
  G = nx.node_link_graph(
    data[0])  # Assuming you only have one document in the collection
  return G


def write_to_file(json_file):
  with open('output.json', 'w') as f:
    json.dump(json_file, f)


def main():
  # Load your data here
  data = read_saturn_file('saturn.111')
  write_to_file(data)
  # Convert data to a graph
  G = convert_to_graph(data)

  uri = "mongodb+srv://testuser:1ONsMdcicJBs2cXz@cluster0.bg2ernm.mongodb.net/crmdb?retryWrites=true&w=majority"
  # Connect to MongoDB Atlas
  client = MongoClient(uri, server_api=ServerApi('1'))
  db = client['Cluster0']  # Use your database name
  collection = db['saturn']  # Use your collection name
  # Write graph to MongoDB
  write_to_mongo(G, collection)
  # Read graph from MongoDB
  G2 = read_from_mongo(collection)
  print(G2.nodes(data=True))
  print(G2.edges(data=True))

  # Send a ping to confirm a successful connection
  try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception as e:
    print(e)

  nx.draw(G, with_labels=True)
  plt.savefig("filename.png")


if __name__ == '__main__':
  main()
