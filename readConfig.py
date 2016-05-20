import json

with open("config.json") as json_file:
    json_data = json.load(json_file)

with open("config.json", 'w') as outfile:
	json.dump(json_data, outfile)
