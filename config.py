import yaml
from box import Box

with open("config.yml", "r") as yml_file:
    cfg = Box(yaml.safe_load(yml_file))
