const fs = require('fs');
const cv = require('../../lib/opencv');
const path = require('path');

// Path ke folder data latih
const trainingDataPath = path.join(__dirname, "../datasets");

// Membaca data latih
const images = [];
const labels = [0, 1, 2];

fs.readdirSync(trainingDataPath).forEach(imageName => {
  if (imageName.endsWith(".jpg")) {
    const imagePath = `${trainingDataPath}/${imageName}`;
    const image = cv.imread(imagePath);
    images.push(image);
  }
});


console.log(cv.LBPHFaceRecognizer)
// Membuat LBPH recognizer dan melatihnya
// const lbphRecognizer = new cv.LBPHFaceRecognizer();
// lbphRecognizer.train(images, labels);

// // Simpan model ke file
// lbphRecognizer.save(path.join(__dirname, '../models/face_recognition_model.yml'), (err) => {
//   if (err) console.error(err);
//   else console.log('Model telah disimpan');
// });
