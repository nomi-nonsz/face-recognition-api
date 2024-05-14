import { Mat, imencode } from "opencv4nodejs-prebuilt-install"
import { getCapture } from "./capture"
import { Socket } from "socket.io-client";

let isConnected = false;

export function inter(io: Socket) {
  if (!isConnected) {
    isConnected = true;
  }
  else {
    console.log("Socket already sended");
    return;
  }

  const cam = getCapture();

  const interval = setInterval(() => {
    const frame: Mat = cam.cap.read();
    if (frame.empty) {
      clearInterval(interval);
      isConnected = false;
    }
    const buffer: string = imencode('.jpg', frame).toString('base64');
    io.emit("cv-detect", buffer);
  }, 1000 / cam.FPS)
}