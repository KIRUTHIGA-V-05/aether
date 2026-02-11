import torch
from ai_engine import ai_engine
from config import config_store

class ResearchKnowledgeRetriever:
    def __init__(self):
        self.corpus_embeddings = None
        self.corpus_segments = []

    def ingest_text(self, text):
        segments = [s.strip() for s in text.split('\n\n') if len(s.strip()) > 30]
        if not segments:
            return
            
        new_embeddings = ai_engine.embed_model.encode(segments, convert_to_tensor=True)
        
        if self.corpus_embeddings is None:
            self.corpus_embeddings = new_embeddings
            self.corpus_segments = segments
        else:
            self.corpus_embeddings = torch.cat((self.corpus_embeddings, new_embeddings), dim=0)
            self.corpus_segments.extend(segments)

    def retrieve_relevant_context(self, query, top_k=config_store.TOP_K_CANDIDATES):
        if self.corpus_embeddings is None:
            return []
            
        query_embedding = ai_engine.embed_model.encode(query, convert_to_tensor=True)
        cos_scores = ai_engine.util.cos_sim(query_embedding, self.corpus_embeddings)[0]
        
        top_results = torch.topk(cos_scores, k=min(top_k, len(self.corpus_segments)))
        
        ranked_context = []
        for score, idx in zip(top_results[0], top_results[1]):
            val = score.item()
            if val >= config_store.RETRIEVAL_THRESHOLD:
                ranked_context.append({
                    "text": self.corpus_segments[idx],
                    "confidence": round(val, 4)
                })
            
        return ranked_context

retriever = ResearchKnowledgeRetriever()