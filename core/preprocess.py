# core/preprocess.py

import spacy
from typing import List, Dict, Any
import json

class Preprocessor:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "lemmatize": True,
            "remove_stopwords": False,
            "custom_stopwords": [],
            "model": "en_core_web_lg"
        }
        self.nlp = spacy.load(self.config.get("model", "en_core_web_lg"))
        self.stopwords = set(self.nlp.Defaults.stop_words).union(set(self.config["custom_stopwords"]))

    def preprocess(self, text: str) -> Dict[str, Any]:
        doc = self.nlp(text)

        sentences = []
        tokens_per_sentence = []

        for sent in doc.sents:
            tokens = []
            for token in sent:
                if self.config["remove_stopwords"] and token.text.lower() in self.stopwords:
                    continue
                tokens.append({
                    "text": token.text,
                    "lemma": token.lemma_ if self.config["lemmatize"] else token.text,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "dep": token.dep_,
                    "head": token.head.text,
                    "ent_type": token.ent_type_,
                    "is_pronoun": token.pos_ == "PRON",
                    "start": token.idx,
                    "end": token.idx + len(token.text)
                })
            sentences.append(sent.text)
            tokens_per_sentence.append(tokens)

        named_entities = [
            {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
            for ent in doc.ents
        ]

        return {
            "sentences": sentences,
            "tokens": tokens_per_sentence,
            "named_entities": named_entities,
            "doc": doc  # Keep doc for downstream reference
        }

# Optional CLI usage
if __name__ == "__main__":
    sample_text = "Angela Merkel met Barack Obama in Berlin. She gave him a gift."
    preprocessor = Preprocessor()
    result = preprocessor.preprocess(sample_text)
    print(json.dumps(result, indent=2))
