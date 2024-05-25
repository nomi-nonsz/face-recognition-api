import cv2 as cv
import base64
import numpy as np
from . import regonite

def detect_face(img: cv.Mat):
  result = regonite.lbph(img)
  _, buffer = cv.imencode('.jpg', result)
  encoded = base64.b64encode(buffer).decode('utf-8')
  mat = result
  return encoded, buffer, mat