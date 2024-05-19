import os
import cv2 as cv
import face_recognition
from . import datasets

def get_face_encodings():
  _datasets = datasets.get_datasets()

  labels = []
  encodings = []
  
  images = os.listdir("datasets")
  for cl in images:
    if any(item["filename"] == cl for item in _datasets) == False:
      continue
    label = [item for item in _datasets if item["filename"] == cl][0]

    if cl.endswith(".jpg") or cl.endswith(".png"):
      curImg = cv.imread(f'datasets/{cl}')
      encode = face_recognition.face_encodings(curImg)[0]
      encodings.append(encode)
      labels.append(label["label"])

  return encodings, labels, _datasets