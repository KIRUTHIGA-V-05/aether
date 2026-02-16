import json
import whisper
import os
import asyncio
from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ppt_generator import generate_ppt_file
from hardware_bridge import get_table_gcode

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = whisper.load_model("base")
session_history = []

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@app.websocket("/ws/{faculty_id}")
async def websocket_endpoint(websocket: WebSocket, faculty_id: str):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)

@app.post("/process_voice/{faculty_id}")
async def process_voice(faculty_id: str, file: UploadFile = File(...)):
    temp_path = f"temp_{faculty_id}.wav"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    result = model.transcribe(temp_path)
    text = result["text"].lower().strip()
    os.remove(temp_path)

    response_data = {
        "type": "BOARD_UPDATE", 
        "content": text, 
        "action": "none",
        "gcode": []
    }

    if "table" in text:
        response_data["action"] = "DRAW_TABLE"
        response_data["content"] = "Aether: Drawing physical table..."
        response_data["gcode"] = get_table_gcode()
    elif "next" in text:
        response_data["action"] = "NEXT_SLIDE"
    elif "highlight" in text:
        response_data["action"] = "HIGHLIGHT"
        response_data["content"] = text.replace("highlight", "").strip()
    
    session_history.append({"intent": response_data["action"], "text": text})
    await manager.broadcast(response_data)
    return {"transcript": text}

@app.get("/generate_summary/{faculty_id}")
async def generate_summary(faculty_id: str):
    file_path = generate_ppt_file(session_history)
    return {"status": "Success", "file_url": file_path}s
