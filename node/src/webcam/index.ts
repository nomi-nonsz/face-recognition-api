import { Mat, imencode } from "opencv4nodejs-prebuilt-install"
import { FPS, cap } from "./capture"
import { io } from "socket.io-client";

function inter() {
  const socket = io("http://localhost:5000");
  const interval = setInterval(() => {
    const frame: Mat = cap.read();
    if (frame.empty) {
      clearInterval(interval);
      socket.disconnect();
    }
    const buffer: string = imencode('.jpg', frame).toString('base64');
    socket.emit("cv-detect", buffer);
  }, 1000 / FPS)
}

inter()