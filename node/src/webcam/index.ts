import { Mat, imencode } from "opencv4nodejs-prebuilt-install"
import { getCapture } from "./capture"
import { Socket } from "socket.io-client";

let isConnected: boolean = false;
let isPlayed: boolean = false;

export function inter(io: Socket) {
  isPlayed = true;
  if (!isConnected) {
    isConnected = true;
  }
  else {
    console.log("Socket is already sended");
    return;
  }

  try {
    const cam = getCapture();
  
    function stop (interval: NodeJS.Timeout) {
      clearInterval(interval);
      isConnected = false;
    }
    const interval = setInterval(() => {
      if (!isPlayed) {
        cam.cap.release();
        stop(interval);
        return;
      }
      const frame: Mat = cam.cap.read();
      if (frame.empty) stop(interval);
      const buffer: string = imencode('.jpg', frame).toString('base64');
      io.emit("cv-detect", buffer);
    }, 1000 / cam.FPS);
  }
  catch (err) {
    if (err == "VideoCapture::New - failed to open capture") {
      console.log("NO CAMERA DETECTED")
    }
    else {
      console.error(err);
    }
  }
}

export function stop () {
  isPlayed = false;
}