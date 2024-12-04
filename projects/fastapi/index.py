from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
from typing import Optional

app = FastAPI()

@app.get("/")
async def home():
    return "Hello, World!"

@app.get("/name")
async def name_route(name: Optional[str] = "Unknown"):
    return f"Hello, {name}!"

@app.post("/post-data")
async def post_data(request: Request):
    data = await request.json()
    print(f"Received data: {data}")
    return data

@app.get("/stream")
async def stream_data():
    async def number_generator():
        for i in range(10):
            yield f"data: {i}\n\n"
            await asyncio.sleep(1)
    
    return StreamingResponse(
        number_generator(),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)