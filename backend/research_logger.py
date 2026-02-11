import json
import os
from datetime import datetime

class ResearchLogger:
    def __init__(self, log_dir="logs/evaluation"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def log_session_metadata(self, config_obj):
        meta = {
            "timestamp": datetime.now().isoformat(),
            "config": {
                "intent_threshold": config_obj.INTENT_THRESHOLD,
                "pattern_threshold": config_obj.PATTERN_THRESHOLD,
                "global_threshold": config_obj.GLOBAL_MIN_CONFIDENCE,
                "weights": [config_obj.INTENT_WEIGHT, config_obj.PATTERN_WEIGHT]
            }
        }
        with open(os.path.join(self.log_dir, "session_config.json"), 'w') as f:
            json.dump(meta, f, indent=4)

    def record_inference(self, input_text, result):
        log_entry = {
            "input": input_text,
            "output": result,
            "timestamp": datetime.now().isoformat()
        }
        filename = f"inference_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(os.path.join(self.log_dir, filename), 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

research_logger = ResearchLogger()