import faiss
from embeddings import create_embeddings, get_query_embedding
from data import documents

# Create embeddings
doc_embeddings = create_embeddings(documents)

# Create FAISS index (cosine similarity)
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)

# Add embeddings to index
index.add(doc_embeddings)

def search(query, top_k=3):
    query_embedding = get_query_embedding(query)
    
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "text": documents[idx],
            "score": float(distances[0][i])
        })
    
    return results