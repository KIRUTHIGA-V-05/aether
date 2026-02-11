import numpy as np
from typing import List, Dict

class StyleEngine:
    def __init__(self):
        self.knowledge_base = {}

    def add_pattern(self, faculty_id: str, problem_type: str, steps: List[str]):
        if faculty_id not in self.knowledge_base:
            self.knowledge_base[faculty_id] = {}
        self.knowledge_base[faculty_id][problem_type] = steps

    def get_structured_solution(self, faculty_id: str, problem_type: str) -> List[Dict]:
        steps = self.knowledge_base.get(faculty_id, {}).get(problem_type, [])
        return [{"step_number": i + 1, "instruction": step} for i, step in enumerate(steps)]

engine = StyleEngine()