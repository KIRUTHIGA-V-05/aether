from fastapi import FastAPI
from pydantic import BaseModel
import re
from intent_config import get_config
from action_planner import planner
from logger_service import logger
from notice_board_manager import notice_manager

app = FastAPI()
config = get_config()

class UserCommand(BaseModel):
    text: str
    faculty_id: str
    mode: str = "BOARD"

@app.post("/process-command")
async def process_command(command: UserCommand):
    raw_text = command.text.lower()
    clean_text = re.sub(rf"\b{config['wake_word']}\b", "", raw_text).strip()
    
    found_intent = "UNKNOWN"
    for intent, keywords in config["intents"].items():
        if any(word in clean_text for word in keywords):
            found_intent = intent
            break

    execution_plan = planner.plan_execution(found_intent, clean_text, command.faculty_id)
    
    notice_update = notice_manager.process_for_notice(clean_text)

    logger.log_action(command.faculty_id, found_intent, {
        "digital_payload": execution_plan,
        "notice": notice_update
    })

    return {
        "agent": "Aether",
        "intent": found_intent,
        "board_action": execution_plan,
        "notice_board_action": notice_update,
        "system_state": {
            "mode": command.mode,
            "session_active": True
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)