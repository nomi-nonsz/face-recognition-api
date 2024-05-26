import recognite
import os
import cv2 as cv
import base64
import socketio
import time

sio = socketio.Client()

def send ():
  sio.connect("http://localhost:5000")
  vid = cv.VideoCapture(os.path.join("examples", "suckomode.mp4"))
  while vid.isOpened():
    ret, frame = vid.read()
    if not ret:
      break
    _, buffer = cv.imencode(".jpg", frame)
    enc = base64.b64encode(buffer).decode('utf-8')
    sio.emit("cv-detect", enc)
    time.sleep(int(vid.get(cv.CAP_PROP_FPS)) / 1000)
  sio.wait()

send()

# recognite.recognite_video(os.path.join("examples", "suckomode.mp4"))
# recognite.recognite(os.path.join("examples", "drake.jpg"))