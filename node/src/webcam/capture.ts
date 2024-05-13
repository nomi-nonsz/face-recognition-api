import * as cv from "opencv4nodejs-prebuilt-install";

export function getCapture (this: any) {
  this.cap = new cv.VideoCapture(0);
  this.width = this.cap.get(cv.CAP_PROP_FRAME_WIDTH);
  this.height = this.cap.get(cv.CAP_PROP_FRAME_HEIGHT);
  this.FPS = 15;
  return this;
}