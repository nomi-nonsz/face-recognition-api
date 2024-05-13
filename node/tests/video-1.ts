import { io } from "socket.io-client";
import * as cv from "opencv4nodejs-prebuilt-install";
import path from 'path';

const socket = io("http://localhost:5000");

const pa = path.join(__dirname + "../../../python/examples/suckomode.mp4");
console.log(pa);
const cap = new cv.VideoCapture(pa);
// const width = cap.get(cv.CAP_PROP_FRAME_WIDTH);
// const height = cap.get(cv.CAP_PROP_FRAME_HEIGHT);
const FPS = 15;

const interval = setInterval(() => {
  const frame: cv.Mat = cap.read();
  if (frame.empty) {
    clearInterval(interval);
    socket.disconnect();
  }
  const buffer: string = cv.imencode('.jpg', frame).toString('base64');
  socket.emit("cv-detect", buffer);
}, 1000 / FPS)