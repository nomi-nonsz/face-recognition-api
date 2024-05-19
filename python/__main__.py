from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
import socketIO_client
import cv2 as cv
import numpy as np
import base64
import threading

import detector

app = Flask(__name__)
CORS(app)
socket = SocketIO(app, cors_allowed_origins="http://localhost:3001")

@socket.on('connect')
def ev_connect():
  sid = request.sid
  print(f"[sid:{sid}] Joined")

@socket.on('disconnect')
def ev_disconnect():
  sid = request.sid
  print(f"[sid:{sid}] Exited")
  cv.destroyAllWindows()

@socket.on('message')
def ev_message(data):
  print(data)

def process_img(data, sid):
  nparr = np.frombuffer(base64.b64decode(data), np.uint8)
  print(f"Loaded buffer: {nparr}")
  img = cv.imdecode(nparr, cv.IMREAD_COLOR)
  if img is None:
    print("Image is Empty")
    return
  result, _, mat = detector.detect_face(img)
  socket.emit("cv-result", result)

@socket.on('cv-detect')
def ev_detect(data):
  sid = request.sid
  # print(f"Receive Response: {data}")

  process_img(data, sid)
  # thread = threading.Thread(target=process_img, args={data, sid})
  # thread.start()

if __name__ == '__main__':
  socket.run(app, port=5000, debug=True)