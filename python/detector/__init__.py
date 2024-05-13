import cv2 as cv
import base64
import numpy as np
from . import regonite

def detect_face(img: cv.Mat):
  result = regonite.regonite(img)
  _, buffer = cv.imencode('.jpg', result)
  encoded = np.array(buffer).tobytes()
  # encoded = base64.b64encode(buffer).decode('utf-8')
  return encoded