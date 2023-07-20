import json

# Define data
data = {
    'server': '192.168.0.0',
    'port': 5556
}

# Write JSON data
with open('config.json', 'w') as f:
    json.dump(data, f, indent=4)
