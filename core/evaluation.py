# core/evaluation.py

from typing import List, Dict
import numpy as np
import itertools
from collections import defaultdict

def b_cubed_score(predicted: List[List[str]], gold: List[List[str]]) -> float:
    mention_to_gold = {}
    for cluster in gold:
        for mention in cluster:
            mention_to_gold[mention] = cluster

    precision_sum = 0
    recall_sum = 0
    total = 0

    for cluster in predicted:
        for mention in cluster:
            if mention not in mention_to_gold:
                continue
            gold_cluster = mention_to_gold[mention]
            overlap = set(cluster).intersection(gold_cluster)
            precision_sum += len(overlap) / len(cluster)
            recall_sum += len(overlap) / len(gold_cluster)
            total += 1

    precision = precision_sum / total if total else 0.0
    recall = recall_sum / total if total else 0.0
    f1 = 2 * precision * recall / (precision + recall + 1e-8)

    return f1

class CorefEvaluator:
    """
    Evaluate predicted chains against gold standard chains using B³ F1.
    Mentions are string-based.
    """

    def __init__(self):
        pass

    def evaluate(self, predicted_chains: List[List[Dict]], gold_chains: List[List[Dict]]) -> Dict[str, float]:
        # Convert each mention to its span string
        pred = [[m["text"] for m in chain] for chain in predicted_chains]
        gold = [[m["text"] for m in chain] for chain in gold_chains]

        return {
            "b3_f1": round(b_cubed_score(pred, gold), 4)
            # You can extend with MUC and CEAF later
        }

#local testing:
# if __name__ == "__main__":
#     evaluator = CorefEvaluator()

#     predicted = [
#         [{"text": "John"}, {"text": "he"}],
#         [{"text": "the store"}]
#     ]

#     gold = [
#         [{"text": "John"}, {"text": "he"}],
#         [{"text": "the store"}]
#     ]

#     scores = evaluator.evaluate(predicted, gold)
#     print("Evaluation:", scores)
