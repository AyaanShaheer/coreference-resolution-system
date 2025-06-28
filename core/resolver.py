from typing import List, Dict, Any
from core.rules import resolve_pronoun
from core.preprocess import Preprocessor
from core.neural_model import NeuralCorefModel


class CoreferenceResolver:
    def __init__(self, use_neural: bool = False):
        self.preprocessor = Preprocessor()
        self.use_neural = use_neural
        self.neural_model = NeuralCorefModel() if use_neural else None

    def extract_mentions(self, tokens_per_sentence: List[List[Dict]], named_entities: List[Dict]) -> List[Dict]:
        """
        Extract noun phrases and pronouns for potential coreference resolution.
        """
        mentions = []

        for sent_idx, tokens in enumerate(tokens_per_sentence):
            for token in tokens:
                if token["pos"] in {"PROPN", "NOUN"}:
                    mentions.append({
                        "text": token["text"],
                        "type": "NP",
                        "sentence_idx": sent_idx,
                        "start": token["start"],
                        "end": token["end"],
                        "number": "plural" if token["tag"] in {"NNS", "NNPS"} else "singular"
                    })
                elif token["is_pronoun"]:
                    mentions.append({
                        "text": token["text"],
                        "type": "PRONOUN",
                        "sentence_idx": sent_idx,
                        "start": token["start"],
                        "end": token["end"]
                    })

        # Annotate entity type (if within NER span)
        for mention in mentions:
            for ent in named_entities:
                if mention["start"] >= ent["start"] and mention["end"] <= ent["end"]:
                    mention["ent_type"] = ent["label"]
                    break

        return mentions

    def resolve_coreferences(self, text: str) -> List[List[Dict]]:
        """
        Resolve coreference chains using either neural or rule-based methods.
        Returns a list of chains; each chain is a list of mentions (dicts).
        """
        data = self.preprocessor.preprocess(text)
        tokens = data["tokens"]
        named_entities = data["named_entities"]
        mentions = self.extract_mentions(tokens, named_entities)

        # Use neural model if enabled
        if self.use_neural and self.neural_model:
            chains = self.neural_model.resolve(text, mentions)
            if chains:
                return chains  # use neural result if it's non-empty

        # Fallback: Rule-based coreference resolution
        chains: List[List[Dict]] = []
        mention_to_chain = {}

        for i, mention in enumerate(mentions):
            if mention["type"] == "PRONOUN":
                antecedent = resolve_pronoun(
                    pronoun=mention["text"],
                    candidate_mentions=[m for m in mentions[:i] if m["type"] == "NP"],
                    sentence_idx=mention["sentence_idx"]
                )

                if antecedent:
                    chain_idx = mention_to_chain.get(id(antecedent))
                    if chain_idx is not None:
                        chains[chain_idx].append(mention)
                        mention_to_chain[id(mention)] = chain_idx
                        continue

            # Start a new chain
            new_chain = [mention]
            chains.append(new_chain)
            mention_to_chain[id(mention)] = len(chains) - 1

        return chains
