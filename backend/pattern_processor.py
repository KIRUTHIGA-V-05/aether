import json
import torch
from ai_engine import ai_engine
from config import config_store

class PatternProcessor:
    def __init__(self, patterns_path="patterns.json"):
        self.patterns_path = patterns_path
        self.patterns_data = self._load_patterns()
        self.pattern_embeddings = {}
        self.metadata = {}
        self._initialize_all_faculty_embeddings()

    def _load_patterns(self):
        with open(self.patterns_path, 'r') as f:
            return json.load(f)

    def _initialize_all_faculty_embeddings(self):
        for faculty_id, intents in self.patterns_data.items():
            faculty_texts = []
            faculty_meta = []
            for intent, items in intents.items():
                for item in items:
                    faculty_texts.append(item["trigger"])
                    faculty_meta.append({
                        "intent": intent,
                        "action": item["action"],
                        "content": item["content"]
                    })
            if faculty_texts:
                self.pattern_embeddings[faculty_id] = ai_engine.embed_model.encode(faculty_texts, convert_to_tensor=True)
                self.metadata[faculty_id] = faculty_meta

    def match_pattern(self, text, faculty_id, top_k=config_store.TOP_K_CANDIDATES):
        if faculty_id not in self.pattern_embeddings:
            return None, 0.0
            
        query_vec = ai_engine.embed_model.encode(text, convert_to_tensor=True)
        similarities = ai_engine.util.cos_sim(query_vec, self.pattern_embeddings[faculty_id])[0]
        
        values, indices = torch.topk(similarities, k=min(top_k, len(self.metadata[faculty_id])))
        
        for i in range(len(values)):
            score = values[i].item()
            if score >= config_store.PATTERN_THRESHOLD:
                return self.metadata[faculty_id][indices[i].item()], score
                
        return None, values[0].item()

processor = PatternProcessor()