import json

def get_datasets():
  stream = open('datasets/datasets.json', 'r')
  data = json.load(stream)
  return data