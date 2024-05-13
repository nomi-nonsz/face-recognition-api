import cv2 as cv
import base64
from . import regonite

def detect_face(img: cv.Mat):
  result = regonite.regonite(img)
  _, buffer = cv.imdecode('.jpg', result)
  encoded = base64.b64encode(buffer).decode('utf-8')
  return encoded