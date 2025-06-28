# tests/test_coref.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from core.resolver import CoreferenceResolver

@pytest.fixture
def resolver():
    return CoreferenceResolver()

def test_basic_resolution(resolver):
    text = "Alice went to the park. She saw a dog."
    chains = resolver.resolve_coreferences(text)
    assert any(
        {"text": "Alice"} in chain and {"text": "She"} in chain
        for chain in chains
    ), "Failed to link 'Alice' and 'She'"

def test_no_resolution(resolver):
    text = "It is raining today."
    chains = resolver.resolve_coreferences(text)
    # Should treat "It" as independent, no antecedent
    assert len(chains) == 1 or all(len(chain) == 1 for chain in chains)

def test_nested_entities(resolver):
    text = "The CEO of Google spoke today. He announced a new policy."
    chains = resolver.resolve_coreferences(text)
    assert any(
        {"text": "He"} in chain for chain in chains
    ), "'He' should resolve to an earlier mention"

def test_multiple_sentences(resolver):
    text = "John met Mary. He greeted her warmly."
    chains = resolver.resolve_coreferences(text)
    mentions = [m["text"] for chain in chains for m in chain]
    assert "John" in mentions and "Mary" in mentions and "He" in mentions and "her" in mentions
