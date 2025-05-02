from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import asyncio
import json

app = FastAPI()

# WebSocket connections to broadcast location updates
connections = []

class Location(BaseModel):
    latitude: float
    longitude: float

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast location to all connected clients
            for connection in connections:
                await connection.send_text(data)
    except WebSocketDisconnect:
        connections.remove(websocket)

@app.post("/update-location")
async def update_location(location: Location):
    location_data = json.dumps(location.dict())
    # Broadcast location data to all WebSocket clients
    for connection in connections:
        await connection.send_text(location_data)
    return {"message": "Location updated successfully!"}

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
