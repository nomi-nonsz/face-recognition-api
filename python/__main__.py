from flask import Flask
from flask_socketio import SocketIO
import socketIO_client
import cv2 as cv
import numpy as np
import base64

import detector

app = Flask(__name__)
socket = SocketIO(app)

@socket.on('connect')
def ev_connect():
  print("Someone joined")

@socket.on('disconnect')
def ev_disconnect():
  print("Someone exit")
  cv.destroyAllWindows()

@socket.on('message')
def ev_message(data):
  print(data)

@socket.on('cv-detect')
def ev_detect(data):
  nparr = np.frombuffer(base64.b64decode(data), np.uint8)
  img = cv.imdecode(nparr, cv.IMREAD_COLOR)
  result = detector.detect_face(img)
  socket.emit("cv-result", result)

if __name__ == '__main__':
  socket.run(app, port=5000, debug=True)