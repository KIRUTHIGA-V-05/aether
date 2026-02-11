from pattern_processor import processor
from ai_engine import ai_engine
from config import config_store

class ActionPlanner:
    def plan_execution(self, text, faculty_id):
        intent, intent_conf = ai_engine.get_top_intent(text)
        pattern_match, pattern_conf = processor.match_pattern(text, faculty_id)
        
        combined_confidence = (intent_conf * config_store.INTENT_WEIGHT) + (pattern_conf * config_store.PATTERN_WEIGHT)
        
        if pattern_match and combined_confidence >= config_store.GLOBAL_MIN_CONFIDENCE:
            return {
                "strategy": "SEMANTIC_PATTERN_EXECUTION",
                "intent": intent,
                "action": pattern_match["action"],
                "data": pattern_match["content"],
                "confidence": round(combined_confidence, 4),
                "metrics": {"intent_conf": round(intent_conf, 4), "pattern_conf": round(pattern_conf, 4)},
                "status": "SUCCESS"
            }
            
        if intent != "UNKNOWN" and intent_conf >= config_store.GLOBAL_MIN_CONFIDENCE:
            return {
                "strategy": "INTENT_ONLY_FALLBACK",
                "intent": intent,
                "action": "GENERIC_DISPLAY",
                "data": text,
                "confidence": round(intent_conf, 4),
                "metrics": {"intent_conf": round(intent_conf, 4), "pattern_conf": round(pattern_conf, 4)},
                "status": "PARTIAL"
            }

        return {
            "strategy": "REJECT_LOW_CONFIDENCE",
            "intent": intent,
            "action": "PROMPT_CLARIFICATION",
            "data": "Input confidence below threshold",
            "confidence": round(combined_confidence, 4),
            "metrics": {"intent_conf": round(intent_conf, 4), "pattern_conf": round(pattern_conf, 4)},
            "status": "FAILED"
        }

planner = ActionPlanner()