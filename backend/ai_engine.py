import whisper
import torch
import numpy as np
from sentence_transformers import SentenceTransformer, util
from config import config_store

class AetherSpeechEngine:
    def __init__(self, model_size="base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.whisper_model = whisper.load_model(model_size, device=self.device)
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
        self.intent_embeddings = {}
        self.util = util

    def transcribe_audio(self, audio_path):
        result = self.whisper_model.transcribe(audio_path, fp16=torch.cuda.is_available())
        return result["text"].strip()

    def set_intent_knowledge(self, intents_dict):
        for intent, examples in intents_dict.items():
            self.intent_embeddings[intent] = self.embed_model.encode(examples, convert_to_tensor=True)

    def get_intent_rankings(self, text):
        if not text or not self.intent_embeddings:
            return [("UNKNOWN", 0.0)]
        
        query_embedding = self.embed_model.encode(text, convert_to_tensor=True)
        rankings = []
        
        for intent, embeddings in self.intent_embeddings.items():
            cos_sim = self.util.cos_sim(query_embedding, embeddings)
            max_score = torch.max(cos_sim).item()
            rankings.append((intent, max_score))
        
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings

    def get_top_intent(self, text):
        rankings = self.get_intent_rankings(text)
        top_intent, top_score = rankings[0]
        if top_score >= config_store.INTENT_THRESHOLD:
            return top_intent, top_score
        return "UNKNOWN", top_score

ai_engine = AetherSpeechEngine()