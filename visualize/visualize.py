# visualize/visualize.py

import streamlit as st
import requests
import json
import random
from typing import List, Dict

API_URL = "http://127.0.0.1:8000/resolve"

def get_color_map(num_chains: int) -> List[str]:
    colors = [
        "#f94144", "#f3722c", "#f8961e", "#f9844a",
        "#f9c74f", "#90be6d", "#43aa8b", "#577590",
        "#277da1", "#9b5de5", "#ff006e", "#8338ec"
    ]
    while len(colors) < num_chains:
        colors += colors
    return colors[:num_chains]

def highlight_text(text: str, chains: List[List[Dict]]) -> str:
    spans = []
    color_map = get_color_map(len(chains))

    for chain_idx, chain in enumerate(chains):
        for mention in chain:
            if isinstance(mention, dict):  # safety check
                spans.append({
                    "start": mention["start"],
                    "end": mention["end"],
                    "color": color_map[chain_idx],
                    "label": chain_idx + 1
                })

    spans = sorted(spans, key=lambda x: x["start"], reverse=True)

    for span in spans:
        highlighted = f"""<span style="background-color: {span['color']}; padding: 2px 4px; border-radius: 4px;" title="Chain {span['label']}">
        {text[span['start']:span['end']]}
        </span>"""
        text = text[:span["start"]] + highlighted + text[span["end"]:]

    return text

# UI setup
st.set_page_config(page_title="Coreference Resolution Visualizer", layout="centered")
st.title("🔗 Coreference Resolution Visualizer")

input_text = st.text_area("Enter text:", height=200, placeholder="e.g. John went to the store. He bought milk.")

if st.button("Resolve Coreferences"):
    if input_text.strip():
        with st.spinner("Resolving..."):
            response = requests.post(API_URL, json={"text": input_text})
            if response.status_code == 200:
                chains = response.json()

                # ✅ Handle stringified JSON if returned that way
                if isinstance(chains, str):
                    try:
                        chains = json.loads(chains)
                    except json.JSONDecodeError:
                        st.error("Could not decode JSON from server.")
                        st.stop()

                st.markdown("### 🔍 Coreference Chains")
                st.markdown(highlight_text(input_text, chains), unsafe_allow_html=True)
            else:
                st.error(f"API Error {response.status_code}: Could not resolve coreferences.")
    else:
        st.warning("Please enter some text.")
