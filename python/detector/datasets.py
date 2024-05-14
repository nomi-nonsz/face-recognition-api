import json

def getDatasets():
  stream = open('datasets/datasets.json', 'r').read()
  data = json.load(stream)
  return data