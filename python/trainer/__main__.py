import cv2 as cv
import os
import numpy as np

from datasets import getDatasets

datasets_dir = "datasets"
trained = "face_model.yml"

images = []
labels = []

def train():
  datasets = getDatasets()
  lists = os.listdir(datasets_dir)

  print("These images will be trained")
  for file in lists:
    if any(item["filename"] == file for item in datasets) == False:
      continue

    label = [item for item in datasets if item["filename"] == file][0]

    if file.endswith(".jpg") or file.endswith(".png"):
      path = os.path.join(datasets_dir, file)
      img = cv.imread(path, cv.IMREAD_GRAYSCALE)
      images.append(img)
      labels.append(label["label"])
      print(path)

  lbphRecognizer = cv.face.LBPHFaceRecognizer_create()
  lbphRecognizer.train(images, np.array(labels))
  lbphRecognizer.save(trained)

  print("Success trained data")

if __name__ == '__main__':
  train()
