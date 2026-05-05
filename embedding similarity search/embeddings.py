from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(documents):
    embeddings = model.encode(documents)
    embeddings = np.array(embeddings).astype('float32')
    
    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)
    
    return embeddings

def get_query_embedding(query):
    embedding = model.encode([query])
    embedding = np.array(embedding).astype('float32')
    
    faiss.normalize_L2(embedding)
    
    return embedding