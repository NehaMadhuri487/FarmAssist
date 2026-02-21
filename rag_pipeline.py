import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load dataset
df = pd.read_csv("data/agriculturedata.csv")

# Convert text to embeddings
embeddings = model.encode(df["content"].tolist())
embeddings = np.array(embeddings).astype("float32")

# Normalize embeddings for cosine similarity
faiss.normalize_L2(embeddings)

# Create FAISS index using Inner Product (cosine similarity)
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)


def search_query(query, top_k=1):
    """
    Returns the most relevant content row(s) for the query.
    Top_k=1 by default for a clean single answer.
    """
    # Encode query
    query_embedding = model.encode([query]).astype("float32")
    faiss.normalize_L2(query_embedding)

    # Search FAISS index
    distances, indices = index.search(query_embedding, top_k)

    # Collect results, avoiding duplicates
    results = []
    seen = set()
    for idx in indices[0]:
        content = df.iloc[idx]["content"]
        if content not in seen:
            results.append(content)
            seen.add(content)

    return results