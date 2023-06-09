import os
import logging
import re


def read_saturn_111(file_name, xy):
  data = {'nodes': [], 'links': []}
  if not os.path.exists(file_name):
    logging.error(f"File {file_name} not found.")
    return data
  with open(file_name, 'r') as file:
    for line in file.readlines():
      if len(line) > 5:  # Skip blank lines
        try:
          if line[:5].isdigit():  # This line represents a node
            id = int(line[0:5])
            node = {
              'id': id,
              'num_links': int(line[6:10]),
              'type': int(line[11:15]),
              'coords': xy.get(
                id,
                (0, 0))  # Use the coordinates if available, otherwise (0, 0)
            }
            data['nodes'].append(node)
          elif line[:5].isspace() and line[5:10].isdigit(
          ):  # This line represents a link
            link = {
              'from':
              int(line[5:10]),
              'to':
              id,
              'num_lanes':
              int(re.sub('[^0-9]', '', line[13:15])),
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
          logging.warning(f"Error parsing 111 line: {ve}")
  return data


def read_coordinate_file(file_name):
  coordinates = {}
  if not os.path.exists(file_name):
    logging.error(f"File {file_name} not found.")
    return coordinates
  with open(file_name, 'r') as file:
    for line in file.readlines():
      parts = line.split()
      if line[0] != 'C':  # Skip blank lines
        try:
          node_id = int(parts[0])  # Assuming node ID is at this position
          coords = (int(parts[1]), int(parts[2])
                    )  # Assuming coordinates are at these positions
          coordinates[node_id] = coords
        except ValueError as ve:
          logging.warning(f"Error parsing 555 line: {ve}")
  return coordinates
