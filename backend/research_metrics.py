import numpy as np
import json
import csv
from datetime import datetime

class ResearchMetricsCalculator:
    def __init__(self, log_path="research_evaluation_results.csv"):
        self.log_path = log_path

    def calculate_summary(self):
        results = []
        with open(self.log_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
        
        thresholds = sorted(list(set(float(r['test_threshold']) for r in results)))
        summary = {}

        for t in thresholds:
            t_subset = [r for r in results if float(r['test_threshold']) == t]
            total = len(t_subset)
            success = len([r for r in t_subset if r['status'] == 'SUCCESS'])
            partial = len([r for r in t_subset if r['status'] == 'PARTIAL'])
            failed = len([r for r in t_subset if r['status'] == 'FAILED'])
            
            rejection_rate = failed / total
            avg_conf = np.mean([float(r['combined_confidence']) for r in t_subset])
            
            summary[t] = {
                "rejection_rate": round(rejection_rate, 4),
                "success_rate": round(success / total, 4),
                "avg_confidence": round(avg_conf, 4),
                "samples": total
            }
        return summary

    def export_ablation_report(self, output_file="ablation_analysis.json"):
        summary = self.calculate_summary()
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=4)

metrics_tool = ResearchMetricsCalculator()