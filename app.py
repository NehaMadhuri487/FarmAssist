from fastapi import FastAPI
from pydantic import BaseModel
from utils import load_kb, load_faiss_index, process_query, retrieve_context
from googletrans import Translator

app = FastAPI(title="Agri Query System")

# Load KB and FAISS
kb_df = load_kb()
faiss_index, embeddings = load_faiss_index()
translator = Translator()

# Request Model
class Query(BaseModel):
    text: str
    lang: str = "auto"

@app.post("/ask")
def ask(query: Query):
    query_text, detected_lang = process_query(query.text)
    context = retrieve_context(query_text, faiss_index, kb_df)
    # Simple concatenation for demonstration (replace with generative AI later)
    response_text = " ".join(context)
    # Translate response back to user language
    if detected_lang != 'en':
        response_text = translator.translate(response_text, src='en', dest=detected_lang).text
    return {"query": query.text, "response": response_text, "language": detected_lang}