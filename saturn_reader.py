import os
import logging


def read_saturn_111(file_name):
  data = {'nodes': [], 'links': []}
  if not os.path.exists(file_name):
    logging.error(f"File {file_name} not found.")
    return data
  with open(file_name, 'r') as file:
    for line in file.readlines():
      if len(line) > 5:  # Skip blank lines
        try:
          if line[5] == " ":  # This line represents a node
            id = int(line[0:5])
            node = {
              'id': id,
              'num_links': int(line[6:10]),
              'type': int(line[11:15])
            }
            data['nodes'].append(node)
          else:  # This line represents a link
            link = {
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
                'first_lane': int(line[32]),
                'last_lane': int(line[34])
              }]
            }
            data['links'].append(link)
        except ValueError as ve:
          logging.warning(f"Error parsing line: {ve}")
  return data


def read_coordinate_file(file_name):
  coordinates = {}
  if not os.path.exists(file_name):
    logging.error(f"File {file_name} not found.")
    return coordinates
  with open(file_name, 'r') as file:
    for line in file.readlines():
      if len(line) > 6 and line[0] != 'C':  # Skip blank lines
        try:
          node_id = int(line[6:11])  # Assuming node ID is at this position
          coords = (int(line[12:20]), int(line[21:29])
                    )  # Assuming coordinates are at these positions
          coordinates[node_id] = coords
        except ValueError as ve:
          logging.warning(f"Error parsing line: {ve}")
  return coordinates
