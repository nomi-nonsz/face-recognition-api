import * as cv from "opencv4nodejs-prebuilt-install";

export const cap = new cv.VideoCapture(0);

export const width = cap.get(cv.CAP_PROP_FRAME_WIDTH);
export const height = cap.get(cv.CAP_PROP_FRAME_HEIGHT);
export const FPS = 15;