# coreference.py

import argparse
import json
from core.resolver import CoreferenceResolver
# from core.neural_model import NeuralCorefModel  # Optional: if integrating neural chains

def main():
    parser = argparse.ArgumentParser(description="Run coreference resolution on input text.")
    parser.add_argument("--input", type=str, required=True, help="Input text or path to a .txt file")
    parser.add_argument("--output", type=str, default="results.json", help="Path to output JSON file")
    parser.add_argument("--use-neural", action="store_true", help="Use neural model for coreference")
    args = parser.parse_args()

    if args.input.endswith(".txt"):
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.input

    resolver = CoreferenceResolver(use_neural=args.use_neural)
    chains = resolver.resolve_coreferences(text)

    result = {
        "text": text,
        "coreference_chains": chains
    }

    with open(args.output, "w", encoding="utf-8") as out_file:
        json.dump(result, out_file, indent=2)
    
    print(f"\n✅ Coreference resolution completed. Results saved to {args.output}\n")

if __name__ == "__main__":
    main()
