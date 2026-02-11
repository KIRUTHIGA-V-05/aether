import torch
from ai_engine import ai_engine
from config import config_store

class SyllabusParser:
    def __init__(self):
        self.syllabus_data = []
        self.syllabus_embeddings = None

    def load_syllabus(self, topic_list):
        self.syllabus_data = topic_list
        if self.syllabus_data:
            self.syllabus_embeddings = ai_engine.embed_model.encode(self.syllabus_data, convert_to_tensor=True)

    def get_closest_topic(self, query_text):
        if self.syllabus_embeddings is None:
            return None, 0.0
            
        query_vec = ai_engine.embed_model.encode(query_text, convert_to_tensor=True)
        similarities = ai_engine.util.cos_sim(query_vec, self.syllabus_embeddings)[0]
        
        max_score, max_idx = torch.max(similarities, dim=0)
        score = max_score.item()
        
        if score >= config_store.SYLLABUS_THRESHOLD:
            return self.syllabus_data[max_idx.item()], score
            
        return None, score

parser = SyllabusParser()