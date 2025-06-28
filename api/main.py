from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.resolver import CoreferenceResolver

app = FastAPI(
    title="Coreference Resolution API",
    description="Resolve coreference chains in English text.",
    version="1.0"
)

# CORS setup to allow frontend access (Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

resolver = CoreferenceResolver(use_neural=False)

class TextInput(BaseModel):
    text: str

@app.post("/resolve")
async def resolve_coreference(input_data: TextInput):
    text = input_data.text.strip()
    if not text:
        return {"error": "Empty input text"}

    chains = resolver.resolve_coreferences(text)
    return chains  # Return raw chains for Streamlit to render correctly

@app.get("/")
def root():
    return {
        "message": "Welcome to the Coreference Resolution API. Use POST /resolve with a JSON {'text': ...}"
    }
