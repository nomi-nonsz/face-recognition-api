import { readFileSync } from 'fs';
import path from 'path';

type Dataset = {
  label: number,
  filename: string,
  name: string
}

export function getDataset (): Dataset[] {
  const stream = readFileSync(path.join(__dirname, "../datasets/datasets.json"), { encoding: 'utf-8' });
  const data: Dataset[] | any[] = JSON.parse(stream);
  return data
}