import csv
import json
import os
import numpy as np

class ResearchAnalyzer:
    def __init__(self, log_path="research_evaluation_results.csv"):
        self.log_path = log_path
        self.results = []
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.log_path):
            return
        with open(self.log_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['test_threshold'] = float(row['test_threshold'])
                row['intent_confidence'] = float(row['intent_confidence'])
                row['pattern_confidence'] = float(row['pattern_confidence'])
                row['combined_confidence'] = float(row['combined_confidence'])
                row['is_correct'] = row['is_correct'].lower() == 'true'
                self.results.append(row)

    def compute_accuracy_tradeoffs(self):
        thresholds = sorted(list(set(r['test_threshold'] for r in self.results)))
        modes = sorted(list(set(r['mode'] for r in self.results)))
        
        analysis = {}
        for mode in modes:
            analysis[mode] = []
            for t in thresholds:
                subset = [r for r in self.results if r['mode'] == mode and r['test_threshold'] == t]
                if not subset: continue
                
                total = len(subset)
                rejected = len([r for r in subset if r['status'] == 'FAILED'])
                accepted = [r for r in subset if r['status'] != 'FAILED']
                
                accuracy = len([r for r in accepted if r['is_correct']]) / len(accepted) if accepted else 0.0
                rejection_rate = rejected / total
                
                analysis[mode].append({
                    "threshold": t,
                    "accuracy": round(accuracy, 4),
                    "rejection_rate": round(rejection_rate, 4),
                    "f1_surrogate": round(2 * (accuracy * (1-rejection_rate)) / (accuracy + (1-rejection_rate) + 1e-9), 4)
                })
        return analysis

    def extract_failure_cases(self):
        failures = [r for r in self.results if not r['is_correct'] and r['status'] != 'FAILED']
        return failures

    def save_report(self, output_path="research_report.json"):
        report = {
            "metrics": self.compute_accuracy_tradeoffs(),
            "critical_failures": self.extract_failure_cases(),
            "summary": {
                "total_samples": len(self.results),
                "unique_modes": list(set(r['mode'] for r in self.results))
            }
        }
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=4)

if __name__ == "__main__":
    analyzer = ResearchAnalyzer()
    analyzer.save_report()