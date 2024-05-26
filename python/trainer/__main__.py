import cv2 as cv
import os
import numpy as np
import pickle
import face_recognition

from datasets import getDatasets

datasets_dir = "datasets"
trained_lbph = "models/lbph_face_model.yml"
trained_hog = "models/hog_face_model.pkl"

images = []
labels = []

def prefixes():
  datasets = getDatasets()
  lists = os.listdir(datasets_dir)
  if os.path.exists("models/") is False:
    os.mkdir("models")
  return datasets, lists

def train_lbph():
  datasets, lists = prefixes()
  print("Training LBPH")
  print("These images will be trained")

  for file in lists:
    if any(item["filename"] == file for item in datasets) == False:
      continue

    label = [item for item in datasets if item["filename"] == file][0]

    if file.endswith(".jpg") or file.endswith(".png"):
      name = label["label"]
      path = os.path.join(datasets_dir, file)
      img = cv.imread(path, cv.IMREAD_GRAYSCALE)
      images.append(img)
      labels.append(name)
      print(f"Label [{name}]: {path}")

  lbphRecognizer = cv.face.LBPHFaceRecognizer_create()
  lbphRecognizer.train(images, np.array(labels))
  lbphRecognizer.save(trained_lbph)
  print("Success trained data")

def train_hog():
  datasets, lists = prefixes()
  print("Training HOG")
  print("These images will be trained")

  for file in lists:
    if any(item["filename"] == file for item in datasets) == False:
      continue

    label = [item for item in datasets if item["filename"] == file][0]

    if file.endswith(".jpg") or file.endswith(".png"):
      name = label["label"]
      path = os.path.join(datasets_dir, file)
      img = face_recognition.load_image_file(path)
      encodings = face_recognition.face_encodings(img)
      if len(encodings) > 0:
        images.append(img)
        labels.append(name)
        print(f"Label [{name}]: {path}")
  
  f = open(trained_hog, 'wb')
  pickle.dump({"encodings": images, "labels": labels}, f)
  print("Training Complete")

if __name__ == '__main__':
  train_lbph()
  train_hog()
