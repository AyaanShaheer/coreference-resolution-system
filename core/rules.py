# core/rules.py

from typing import List, Dict, Optional

# Basic gender mapping for pronouns
GENDER_PRONOUNS = {
    "he": "male",
    "him": "male",
    "his": "male",
    "she": "female",
    "her": "female",
    "hers": "female",
    "they": "neutral",
    "them": "neutral",
    "their": "neutral",
    "it": "neutral",
    "its": "neutral"
}

def get_gender(word: str) -> Optional[str]:
    return GENDER_PRONOUNS.get(word.lower())

def is_potential_antecedent(pronoun: str, candidate: Dict) -> bool:
    """
    Checks gender agreement between pronoun and candidate mention.
    """
    pronoun_gender = get_gender(pronoun)
    if pronoun_gender and "gender" in candidate:
        return candidate["gender"] == pronoun_gender
    return True  # If gender unknown, assume possible

def resolve_pronoun(pronoun: str, candidate_mentions: List[Dict], sentence_idx: int) -> Optional[Dict]:
    best_candidate = None
    best_score = -1

    for candidate in candidate_mentions:
        if candidate["sentence_idx"] > sentence_idx:
            continue

        score = 0

        # Rule 1: Gender match
        if is_potential_antecedent(pronoun, candidate):
            score += 1

        # Rule 2: Entity type preference (e.g., prefer PERSON for 'he'/'she')
        pronoun_gender = get_gender(pronoun)
        if pronoun_gender in {"male", "female"}:
            if candidate.get("ent_type") == "PERSON":
                score += 1

        # Rule 3: Number agreement
        if candidate.get("number", "unknown") == "singular":
            score += 1

        # Rule 4: Proximity
        score -= (sentence_idx - candidate["sentence_idx"])

        if score > best_score:
            best_score = score
            best_candidate = candidate

    return best_candidate
