import express from 'express';
import http from 'http';
import cors from 'cors';
import * as socketio from 'socket.io';
import * as socketio_client from 'socket.io-client';
import path from 'path';
import { config } from 'dotenv';

import { inter } from './webcam';

config();

const app: express.Express = express();
const server: http.Server = http.createServer(app);
const io: socketio.Server = new socketio.Server({
  cors: {
    origin: process.env['PYTHON_URL'] || "*"
  }
});

const io_client = socketio_client.io(process.env['PYTHON_URL'] || 'http://localhost:5000');

const port = 3000;
const host = 'localhost';

app.use(cors({ origin: "*" }));
app.use(express.static(path.join(__dirname, "public")));

app.post("/webcam", (req: express.Request, res: express.Response) => {
  inter();
  res.sendStatus(200);
})

io_client.on('cv-result', (data) => {
  app.get('/image', (req: express.Request, res: express.Response) => {
    const header = {
      "Content-Type": "image/jpg",
      "Accept-Ranges": "bytes"
    }
    res.writeHead(200, header)
    res.send(data);
  })
})

server.listen(port, host, () => {
  console.log(`Node.js Server is running at http://${host}:${port}`);
})