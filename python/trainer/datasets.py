import json
import os

def getDatasets() -> list:
  stream = open("./datasets/datasets.json", "r")
  data = json.load(stream)
  return data