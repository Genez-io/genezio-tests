import asyncio
import websockets

PORT = 8765

async def handle_connection(websocket):
    try:
        await websocket.send("Welcome to the WebSocket server!")
        
        async for message in websocket:
            print(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")
            
    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Error handling connection: {e}")
        if not websocket.closed:
            await websocket.close(1011)

async def main():
    async with websockets.serve(handle_connection, "localhost", PORT):  
        print(f"WebSocket server is running on ws://localhost:{PORT}")
        await asyncio.Future() 

asyncio.run(main())
