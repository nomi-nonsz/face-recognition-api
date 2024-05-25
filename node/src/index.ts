import express from 'express';
import http from 'http';
import cors from 'cors';
import * as socketio from 'socket.io';
import * as socketio_client from 'socket.io-client';
import path from 'path';
import { config } from 'dotenv';
import { writeFileSync } from 'fs';

import * as webcam from './webcam';

config();

const app: express.Express = express();
const server: http.Server = http.createServer(app);
const io: socketio.Server = new socketio.Server({
  cors: {
    origin: process.env['PYTHON_URL'] || "*"
  }
});

const io_client = socketio_client.io(process.env['PYTHON_URL'] || 'http://localhost:5000');

const port = 3001;
const host = 'localhost';

app.use(cors({ origin: "*" }));
app.use(express.static(path.join(__dirname, "public")));

app.post("/webcam/:action", (req: express.Request, res: express.Response) => {
  const act = req.params["action"];

  switch (act) {
    case "true":
      console.log("Starting webcam");
      webcam.inter(io_client);
      break;
    case "false":
      console.log("Stopping webcam");
      webcam.stop();
      break;
    default:
      res.status(400).send("It must be true/false value");
      return;
  }

  res.sendStatus(200);
})

// io_client.on('cv-result', (data) => {
//   writeFileSync(__dirname + "/public/example.jpg", data, 'base64');
//   console.log(`Writed File ${__dirname + "/public/example.jpg"}`)
// })

server.listen(port, host, () => {
  console.log(`Node.js Server is running at http://${host}:${port}`);
})