# core/neural_model.py

import torch
from transformers import AutoTokenizer, AutoModel
from typing import Dict, List, Optional
import numpy as np

class NeuralCorefModel:
    def __init__(self, model_name: str = "roberta-base", device: str = None):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def encode(self, text: str) -> torch.Tensor:
        """Returns contextual embeddings for the text."""
        tokens = self.tokenizer(text, return_tensors="pt", truncation=True)
        tokens = {k: v.to(self.device) for k, v in tokens.items()}
        with torch.no_grad():
            output = self.model(**tokens)
        return output.last_hidden_state.mean(dim=1).squeeze(0)  # [hidden_size]

    def score_pair(self, mention1: str, mention2: str) -> float:
        """Score whether two mentions refer to the same entity."""
        vec1 = self.encode(mention1)
        vec2 = self.encode(mention2)
        similarity = torch.nn.functional.cosine_similarity(vec1, vec2, dim=0)
        return similarity.item()  # Float score

    def resolve(self, pronoun: str, candidates: List[Dict]) -> Optional[Dict]:
        """Choose the best antecedent using similarity scoring."""
        best_score = -1.0
        best_candidate = None

        for candidate in candidates:
            score = self.score_pair(pronoun, candidate["text"])
            if score > best_score:
                best_score = score
                best_candidate = candidate

        return best_candidate if best_score > 0.6 else None  # Threshold for confidence
