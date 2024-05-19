from recognite import recognite_self2
import socketio
import cv2 as cv
import base64
import threading

sio = socketio.Client()

# def webcam():
#   sio.connect("http://localhost:5000"
#   cap = cv.VideoCapture(0)
#   while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#       break
#     _, buffer = cv.imencode(".jpg", frame)
#     enc = base64.b64encode(buffer).decode('utf-8')
#     sio.emit('cv-detect', enc)
#   sio.wait()

recognite_self2()