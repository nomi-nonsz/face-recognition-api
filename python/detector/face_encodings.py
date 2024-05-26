import os
import cv2 as cv
import face_recognition
import pickle
from . import datasets

def get_face_encodings():
  _datasets = datasets.get_datasets()

  labels = []
  encodings = []

  with open("models/hog_face_model.pkl", 'rb') as f:
    data = pickle.load(f)
    encodings = data["encodings"]
    labels = data["labels"]

  return encodings, labels, _datasets