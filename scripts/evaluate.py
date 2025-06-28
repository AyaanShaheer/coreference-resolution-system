# scripts/evaluate.py

import json
from core.evaluation import CorefEvaluator
from core.resolver import CoreferenceResolver

# Sample input for testing
sample_text = "John went to the store. He bought some milk."

# Gold coreference chains for sample_text
gold_chains = [
    [{"text": "John"}, {"text": "He"}],
    [{"text": "the store"}]
]

def main():
    resolver = CoreferenceResolver()
    evaluator = CorefEvaluator()

    # Get predicted chains from resolver
    predicted_chains = resolver.resolve_coreferences(sample_text)

    # Evaluate
    scores = evaluator.evaluate(predicted_chains, gold_chains)

    print("\n📊 Evaluation Results:")
    print(json.dumps(scores, indent=4))

if __name__ == "__main__":
    main()
