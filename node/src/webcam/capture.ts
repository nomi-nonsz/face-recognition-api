import * as cv from "opencv4nodejs-prebuilt-install";

export function getCapture () {
  const cap = new cv.VideoCapture(0);
  const width = cap.get(cv.CAP_PROP_FRAME_WIDTH);
  const height = cap.get(cv.CAP_PROP_FRAME_HEIGHT);
  const FPS = 30;
  return { cap, width, height, FPS };
}