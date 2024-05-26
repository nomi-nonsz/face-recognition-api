import cv2 as cv
from . import face_encodings, datasets
import numpy as np
import face_recognition

# Skala ukuran 1:_SCALE
_SCALE = 1

recogniter = cv.face.LBPHFaceRecognizer_create()
recogniter.read("models/lbph_face_model.yml")
cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

labels = datasets.get_datasets()
_face_r_encodings, _face_r_labels, _face_r_datasets = face_encodings.get_face_encodings()

def lbph(img: cv.Mat) -> cv.Mat:
  s_img = cv.resize(img, (0, 0), None, 1/_SCALE, 1/_SCALE)
  g_img = cv.cvtColor(s_img, cv.COLOR_BGR2GRAY)
  faces = cascade.detectMultiScale(g_img, scaleFactor=1.1, minNeighbors=5)

  for (x, y, w, h) in faces:
    face_reg = g_img[y:y+h, x:x+w]
    label, conf = recogniter.predict(face_reg)
    g_color = (0, 255, 0)
    g_stroke = 2
    _label = [item for item in labels if item["label"] == label][0]
    x, y, w, h = x*_SCALE, y*_SCALE, w*_SCALE, h*_SCALE

    if conf > 0:
      cv.rectangle(img, (x, y), (x+w, y+h), g_color, g_stroke)
      cv.putText(img, _label["name"] or "Undifined", (x, y+(y*3+3)), cv.FONT_HERSHEY_SIMPLEX, 0.5, g_color, g_stroke)

  return img

def hog(frame: cv.Mat):
  s_frame = cv.resize(frame, (0, 0), None, 1/_SCALE, 1/_SCALE)
  facesCurFrame = face_recognition.face_locations(s_frame)
  encodesCurFrame = face_recognition.face_encodings(s_frame, facesCurFrame)

  for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
    matches = face_recognition.compare_faces(_face_r_encodings, encodeFace)
    faceDis = face_recognition.face_distance(_face_r_encodings, encodeFace)
    matchIndex = np.argmin(faceDis)

    if matches[matchIndex]:
      name = _face_r_datasets[matchIndex]["name"]

      y1, x2, y2, x1 = faceLoc
      y1, x2, y2, x1 = y1*_SCALE, x2*_SCALE, y2*_SCALE, x1*_SCALE
      
      cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
      cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
      cv.putText(frame, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

  return frame