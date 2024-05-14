import cv2 as cv
import face_encodings
import numpy as np
import face_recognition

recogniter = cv.face.LBPHFaceRecognizer_create()
recogniter.read("face_model.yml")
cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

_face_r_encodings, _face_r_labels = face_encodings.get_face_encodings()

def regonite(img: cv.Mat) -> cv.Mat:
  g_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  faces = cascade.detectMultiScale(g_img, scaleFactor=1.1, minNeighbors=5)

  for (x, y, w, h) in faces:
    face_reg = g_img[y:y+h, x:x+w]
    label, conf = recogniter.predict(face_reg)

    g_color = (0, 255, 0)
    g_stroke = 2

    if conf > 40:
      cv.rectangle(img, (x, y), (x+w, y+h), g_color, g_stroke)
      cv.putText(img, str(label), (x, y+(y*3+3)), cv.FONT_HERSHEY_SIMPLEX, 0.5, g_color, g_stroke)

  return img

def regonite_alt(frame: cv.Mat):
  facesCurFrame = face_recognition.face_locations(frame)
  encodesCurFrame = face_recognition.face_encodings(frame, facesCurFrame)

  for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
      matches = face_recognition.compare_faces(_face_r_encodings, encodeFace)
      faceDis = face_recognition.face_distance(_face_r_encodings, encodeFace)
      matchIndex = np.argmin(faceDis)

      if matches[matchIndex]:
        name = _face_r_labels[matchIndex].name
        y1, x2, y2, x1 = faceLoc
        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
        cv.putText(frame, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

  return frame