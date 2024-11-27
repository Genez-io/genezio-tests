import { WebSocketServer } from 'ws';

const PORT = 8080;
const wss = new WebSocketServer({ port: PORT }, () => {
  console.log(`WebSocket server is running on ws://localhost:${PORT}`);
});

wss.on('connection', (ws) => {
  ws.on('message', (message) => {
    // Echo back the received message
    ws.send(`Echo: ${message}`);
  });

  ws.send('Welcome to the WebSocket server!');
});

