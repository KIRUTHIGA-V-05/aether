from fastapi import FastAPI, UploadFile, File, Body
from pydantic import BaseModel
from ai_engine import ai_engine
from action_planner import planner
from intent_config import get_config
from knowledge_retriever import retriever
import os

app = FastAPI()

config = get_config()
ai_engine.set_intent_knowledge(config["intents"])

class CommandRequest(BaseModel):
    text: str
    faculty_id: str

@app.post("/process-voice")
async def process_voice(file: UploadFile = File(...), faculty_id: str = Body(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    transcript = ai_engine.transcribe_audio(temp_path)
    os.remove(temp_path)
    
    execution_plan = planner.plan_execution(transcript, faculty_id)
    
    return {
        "raw_transcript": transcript,
        "analysis": execution_plan
    }

@app.post("/process-text")
async def process_text(request: CommandRequest):
    execution_plan = planner.plan_execution(request.text, request.faculty_id)
    return execution_plan

@app.post("/ingest-research-data")
async def ingest_data(content: str = Body(..., embed=True)):
    retriever.ingest_text(content)
    return {"status": "Knowledge Base Updated", "segments": len(retriever.corpus_segments)}

@app.get("/system-health")
async def health():
    return {
        "device": ai_engine.device,
        "cuda_active": torch.cuda.is_available(),
        "memory_allocated": f"{torch.cuda.memory_allocated(0)/1024**2:.2f}MB" if torch.cuda.is_available() else "N/A"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)