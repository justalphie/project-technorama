import sys, yaml, json
with open('sections_with_details.json', 'r') as json_file:
    data = json.load(json_file)

with open('sections_with_details.yaml', 'w') as yaml_file:
    yaml.dump(data, yaml_file)