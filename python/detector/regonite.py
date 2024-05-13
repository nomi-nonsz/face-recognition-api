import cv2 as cv
import os

def regonite(img: cv.Mat) -> cv.Mat:
  recogniter = cv.face.LBPHFaceRecognizer_create()
  recogniter.read("face_model.yml")
  cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
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
