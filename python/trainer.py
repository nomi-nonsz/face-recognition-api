import cv2 as cv
import os
import numpy as np

datasets = "datasets"
trained = "face_model.yml"

images = []
labels = [0, 1, 2]

lists = os.listdir(datasets)

print("These images will be trained")
for data in lists:
  if data.endswith(".jpg") or data.endswith(".png"):
    path = os.path.join(datasets, data)
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    images.append(img)
    print(path)

lbphRecognizer = cv.face.LBPHFaceRecognizer_create()
lbphRecognizer.train(images, np.array(labels))

lbphRecognizer.save(trained)

print("Success trained data")
