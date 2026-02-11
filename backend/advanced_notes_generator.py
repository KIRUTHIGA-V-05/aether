import json
from datetime import datetime

class NotesGenerator:
    def __init__(self, session_id):
        self.session_id = session_id
        self.header = f"SESSION REPORT: {session_id}\nDATE: {datetime.now().strftime('%Y-%m-%d')}\n"

    def format_as_markdown(self, logs):
        md_output = self.header + "===\n\n"
        for entry in logs:
            intent = entry.get("intent")
            data = entry.get("data", {}).get("data", {})
            
            if intent == "ACTION_WRITE":
                md_output += f"### Key Concept\n> {data.get('text')}\n\n"
            elif intent == "ACTION_SOLVE_PATTERN":
                md_output += "### Step-by-Step Solution\n"
                for step in data:
                    md_output += f"{step['step']}. {step['content']}\n"
                md_output += "\n"
        
        with open(f"notes_{self.session_id}.md", "w") as f:
            f.write(md_output)
        return md_output

notes_gen = NotesGenerator("CLASS_WEB_PROG_001")