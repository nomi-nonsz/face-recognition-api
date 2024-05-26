import cv2 as cv
import face_recognition
import os
import numpy as np
import base64
import socketio
import threading

io = socketio.Client()

labels = ["Drake", "Elon", "Ryan Gosling", "Linus Torvalds"]

def reco(img_colored):
  recognizer = cv.face.LBPHFaceRecognizer_create()
  recognizer.read("models/face_model.yml")

  img = cv.cvtColor(img_colored, cv.COLOR_BGR2GRAY)

  classifier = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')
  # classifier = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
  rects = classifier.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)

  for (x, y, w, h) in rects:
    face_region = img[y:y+h, x:x+w]
    label_id, confidence = recognizer.predict(face_region)

    rect_color = (0, 255, 0)
    rect_stroke = 2

    if confidence > 40:
      cv.rectangle(img_colored, (x, y), (x+w, y+h), rect_color, rect_stroke)
      cv.putText(img_colored, f"{label_id}: {labels[label_id]}", (x, y+h+28), cv.FONT_HERSHEY_SIMPLEX, 0.8, rect_color, rect_stroke)
    else:
      cv.rectangle(img_colored, (x, y), (x+w, y+h), rect_color, rect_stroke)
      cv.putText(img_colored, "Idk who is this", (x, y+h+28), cv.FONT_HERSHEY_SIMPLEX, 0.8, rect_color, rect_stroke)


def recognite(path):
  img_colored = cv.imread(path)
  reco(img_colored)

  cv.imshow('Face recognition', img_colored)
  cv.waitKey(0)
  cv.destroyAllWindows()

def recognite_video(path):
  io.connect('http://localhost:5000')

  cap = cv.VideoCapture(path)

  # frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
  # frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
  # fps = cap.get(cv.CAP_PROP_FPS)

  while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
      break

    reco(frame)

    # cv.imshow('Face recognition Video', frame)
    _, buffer = cv.imencode(".jpg", frame)
    encoded = base64.b64encode(buffer).decode('utf-8')

    io.emit("cv-detect", encoded)

    if cv.waitKey(1) & 0xFF == ord('q'):
      break


def recognite_self():
  cap = cv.VideoCapture(0)

  # frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
  # frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
  # fps = cap.get(cv.CAP_PROP_FPS)

  while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
      break

    reco(frame)

    cv.imshow('Face recognition Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
      break

def recognite_self2():
  size_scale = 4
  cap = cv.VideoCapture(0)

  labels = ["Linus", "Drake", "Elon", "Ryan Gosling"]
  encodings = []
  images = os.listdir("datasets")
  labels = []
  for cl in images:
    if cl.endswith(".jpg"):
      curImg = cv.imread(f'datasets/{cl}')
      encode = face_recognition.face_encodings(curImg)[0]
      encodings.append(encode)
      labels.append(cl)

  # frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
  # frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
  # fps = cap.get(cv.CAP_PROP_FPS)

  while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
      break

    frame_smoll = cv.resize(frame, (0, 0), None, 1/size_scale, 1/size_scale)

    facesCurFrame = face_recognition.face_locations(frame_smoll)
    encodesCurFrame = face_recognition.face_encodings(frame_smoll, facesCurFrame)
 
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
      matches = face_recognition.compare_faces(encodings, encodeFace)
      faceDis = face_recognition.face_distance(encodings, encodeFace)
      matchIndex = np.argmin(faceDis)

      if matches[matchIndex]:
        name = labels[matchIndex]
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*size_scale, x2*size_scale, y2*size_scale, x1*size_scale
        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
        cv.putText(frame, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv.imshow('Face recognition Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
      break


def recognite2(path):
  labels = ["Drake", "Elon", "Ryan Gosling"]
  encodings = []
  images = os.listdir("datasets")
  
  for cl in images:
    curImg = cv.imread(f'datasets/{cl}')
    encode = face_recognition.face_encodings(curImg)[0]
    encodings.append(encode)

  img = cv.imread(path)

  facesCurFrame = face_recognition.face_locations(img)
  encodesCurFrame = face_recognition.face_encodings(img, facesCurFrame)

  for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
      matches = face_recognition.compare_faces(encodings, encodeFace)
      faceDis = face_recognition.face_distance(encodings, encodeFace)
      matchIndex = np.argmin(faceDis)

      if matches[matchIndex]:
        print("Match!")
        name = labels[matchIndex]
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 1, x2 * 1, y2 * 1, x1 * 1
        cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
        cv.putText(img, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

  cv.imshow('Face recognition Video', img)

  cv.waitKey(0)
  cv.destroyAllWindows()

def recognite_video2(path):
  cap = cv.VideoCapture(path)

  # frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
  # frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
  # fps = cap.get(cv.CAP_PROP_FPS)

  labels = ["Drake", "Elon", "Ryan Gosling"]
  encodings = []
  images = os.listdir("datasets")
  for cl in images:
    curImg = cv.imread(f'datasets/{cl}')
    encode = face_recognition.face_encodings(curImg)[0]
    encodings.append(encode)

  while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
      break

    facesCurFrame = face_recognition.face_locations(frame)
    encodesCurFrame = face_recognition.face_encodings(frame, facesCurFrame)
 
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodings, encodeFace)
        faceDis = face_recognition.face_distance(encodings, encodeFace)
        matchIndex = np.argmin(faceDis)
 
        if matches[matchIndex]:
          name = labels[matchIndex]
          y1, x2, y2, x1 = faceLoc
          cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
          cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
          cv.putText(frame, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv.imshow('Face recognition Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
      break