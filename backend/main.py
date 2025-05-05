from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from azure_api import query_azure_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = query_azure_api(data)
        await websocket.send_text(response)
