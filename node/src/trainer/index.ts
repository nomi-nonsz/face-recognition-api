import { Mat, LBPHFaceRecognizer, imread } from 'opencv4nodejs-prebuilt-install';
import { lstatSync, readdirSync } from 'fs';
import path from 'path';
import { getDataset } from './datasets';

const modelPath: string = path.join(__dirname, "../models");
const datasetsPath: string = path.join(__dirname, "../datasets");

const images: Mat[] = [];
const labels: number[] = [];

function train (): void {
  const datasets = getDataset();
  const files: string[] = readdirSync(datasetsPath);
  
  files.forEach(file => {
    const data = datasets.find(d => d.filename == file);
    
    if ((file.endsWith(".jpg") || file.endsWith(".png")) && data) {

      const imgPath: string = `${datasetsPath}/${file}`;
      const image: Mat = imread(imgPath);
  
      const label: number = data.label;
      images.push(image);
      labels.push(label);
    }
  })

  console.log(LBPHFaceRecognizer)
  // const lbpReco = new LBPHFaceRecognizer();

  // lbpReco.train(images, labels);
  // lbpReco.save(`${modelPath}/face_model.yml`);
}

train();