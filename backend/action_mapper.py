from style_engine import engine

class ActionMapper:
    def __init__(self):
        self.current_mode = "BOARD"

    def map_to_json(self, intent: str, entity: str, faculty_id: str):
        if intent == "ACTION_SOLVE_PATTERN":
            steps = engine.get_structured_solution(faculty_id, entity)
            return {
                "type": "SEQUENCE",
                "mode": self.current_mode,
                "data": steps
            }
        
        if intent == "ACTION_WRITE":
            return {
                "type": "CANVAS_TEXT",
                "mode": "BOARD",
                "data": {"content": entity}
            }
            
        return {"type": "UNKNOWN", "mode": self.current_mode, "data": {}}

mapper = ActionMapper()