import json
import os

class KnowledgeIngestor:
    def __init__(self, storage_path="patterns.json"):
        self.storage_path = storage_path

    def save_faculty_method(self, faculty_id: str, problem_type: str, steps: list):
        current_data = {}
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                current_data = json.load(f)
        
        if faculty_id not in current_data:
            current_data[faculty_id] = {}
            
        current_data[faculty_id][problem_type.lower()] = steps
        
        with open(self.storage_path, "w") as f:
            json.dump(current_data, f, indent=4)
        return True

ingestor = KnowledgeIngestor()