import json

temp = open('.env', 'r')
temp = temp.readline()
env_directory = temp.split('\n')[0][10:] + '/pi.json'

JSON_FILE = env_directory

def get_directory_from_alias(alias):
  with open(JSON_FILE) as json_file:
    data = json.load(json_file)
    return (data.get(alias, None))

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

def get_all():
  with open(JSON_FILE) as json_file:
    data = json.load(json_file)
    if len(data) < 1:
      return "No aliases currently added!"
    formatted_data = "\n".join(f"{alias}: '{directory}'" for alias, directory in data.items())
  return formatted_data