import csv
import os
import torch
from ai_engine import ai_engine
from pattern_processor import processor
from action_planner import planner
from config import config_store

class ThresholdEvaluator:
    def __init__(self):
        self.test_cases = [
            {"text": "Aether write photosynthesis", "faculty_id": "FACULTY_01", "label": "WRITE"},
            {"text": "Solve area of circle", "faculty_id": "FACULTY_01", "label": "SOLVE"},
            {"text": "Go to next slide", "faculty_id": "FACULTY_01", "label": "NAVIGATE"},
            {"text": "Random noise background", "faculty_id": "FACULTY_01", "label": "UNKNOWN"},
            {"text": "Show chart of results", "faculty_id": "FACULTY_01", "label": "WRITE"},
            {"text": "Explain binary search", "faculty_id": "FACULTY_01", "label": "WRITE"},
            {"text": "Next page", "faculty_id": "FACULTY_01", "label": "NAVIGATE"},
            {"text": "Blah blah signal", "faculty_id": "FACULTY_01", "label": "UNKNOWN"}
        ]
        self.output_file = "research_evaluation_results.csv"

    def run_ablation_sweep(self, modes=["FULL", "INTENT_ONLY", "PATTERN_ONLY"]):
        threshold_range = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        
        with open(self.output_file, mode='w', newline='') as csvfile:
            fieldnames = [
                'mode', 'test_threshold', 'input_text', 'label', 
                'predicted_intent', 'intent_confidence', 
                'pattern_confidence', 'combined_confidence', 
                'strategy', 'status', 'is_correct'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            orig_i_w = config_store.INTENT_WEIGHT
            orig_p_w = config_store.PATTERN_WEIGHT

            for mode in modes:
                if mode == "INTENT_ONLY":
                    config_store.INTENT_WEIGHT, config_store.PATTERN_WEIGHT = 1.0, 0.0
                elif mode == "PATTERN_ONLY":
                    config_store.INTENT_WEIGHT, config_store.PATTERN_WEIGHT = 0.0, 1.0
                else:
                    config_store.INTENT_WEIGHT, config_store.PATTERN_WEIGHT = orig_i_w, orig_p_w

                for t in threshold_range:
                    config_store.GLOBAL_MIN_CONFIDENCE = t
                    for case in self.test_cases:
                        res = planner.plan_execution(case["text"], case["faculty_id"])
                        is_correct = (res["intent"] == case["label"])
                        
                        writer.writerow({
                            'mode': mode,
                            'test_threshold': t,
                            'input_text': case["text"],
                            'label': case["label"],
                            'predicted_intent': res["intent"],
                            'intent_confidence': res["metrics"]["intent_conf"],
                            'pattern_confidence': res["metrics"]["pattern_conf"],
                            'combined_confidence': res["confidence"],
                            'strategy': res["strategy"],
                            'status': res["status"],
                            'is_correct': is_correct
                        })

            config_store.INTENT_WEIGHT = orig_i_w
            config_store.PATTERN_WEIGHT = orig_p_w

if __name__ == "__main__":
    evaluator = ThresholdEvaluator()
    evaluator.run_ablation_sweep()