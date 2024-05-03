import json
import os

# This variable is used to get the path of the JSON file that stores the aliases and their corresponding directories, no matter what directory the script is called from.
curr_dir = os.path.dirname(os.path.abspath(__file__))

JSON_FILE = curr_dir + '/pi.json'

# Function to get the directory from the alias provided from the JSON file
def get_directory_from_alias(alias):
  with open(JSON_FILE) as json_file:
    data = json.load(json_file)
    return (data.get(alias, None))

# Function to add a new alias and directory pair to the JSON file
def add_entry(alias, directory):
  try:
    with open(JSON_FILE, 'r') as json_file:
      data = json.load(json_file)

    data[alias] = directory

    with open(JSON_FILE, 'w') as json_file:
      json.dump(data, json_file, indent=2)

    return True
  except Exception as e:
    return False

# Function to remove an alias from the JSON file
def remove_entry(alias):
  try:
    with open(JSON_FILE, 'r') as json_file:
      data = json.load(json_file)
    if alias in data:
      del data[alias]
      with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, indent=2)
      return True
    else:
      return False
  except Exception as e:
    return False

# Function to list all the aliases and their corresponding directories
def get_all():
  with open(JSON_FILE) as json_file:
    data = json.load(json_file)
    if len(data) < 1:
      return "No aliases currently added!"
    formatted_data = "\n".join(f"{alias}: '{directory}'" for alias, directory in data.items())
  return formatted_data

# Function to get the Github token from .env file assuming it has already been added
def get_github_token():
  with open(f'{curr_dir}/.env', 'r') as file:
    lines = file.readlines()
    token = lines[1].split('=')[1].strip()
    return token
  