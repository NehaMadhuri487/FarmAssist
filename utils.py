import pandas as pd
import numpy as np
import faiss
import torch
from sentence_transformers import SentenceTransformer
from langdetect import detect
from googletrans import Translator

# Load Sentence Transformer Model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize translator
translator = Translator()

# Load Knowledge Base
def load_kb(path='kb.csv'):
    df = pd.read_csv(path)
    return df

# Generate embeddings for KB if not already done
def build_faiss_index(df):
    embeddings = embedder.encode(df['text'].tolist(), convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, 'faiss_index.bin')
    np.save('embeddings.npy', embeddings)
    return index, embeddings

# Load existing FAISS index
def load_faiss_index():
    index = faiss.read_index('faiss_index.bin')
    embeddings = np.load('embeddings.npy')
    return index, embeddings

# Query processing: detect language, translate to English if needed
def process_query(query, target_lang='en'):
    lang = detect(query)
    if lang != 'en':
        query_en = translator.translate(query, src=lang, dest='en').text
    else:
        query_en = query
    return query_en, lang

# Retrieve top k relevant KB entries
def retrieve_context(query, index, df, k=5):
    query_vec = embedder.encode([query], convert_to_numpy=True)
    distances, idxs = index.search(query_vec, k)
    return df.iloc[idxs[0]]['text'].tolist()