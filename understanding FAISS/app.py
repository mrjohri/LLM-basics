from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load documents
with open("data/documents.txt", "r", encoding="utf-8") as f:
    documents = [doc.strip() for doc in f.readlines()]

# Convert text -> embeddings
embeddings = np.array(model.encode(documents)).astype('float32')

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print(f"Total documents indexed: {index.ntotal}")

# Save index
faiss.write_index(index, "db/faiss_index.bin")
with open("db/texts.pkl", "wb") as f:
    pickle.dump(documents, f)

print("Vector DB saved!")

# Query section
while True:
    query = input("\nEnter your query (or type exit): ")

    if query.lower() == "exit":
        break

    query_embedding = np.array(model.encode([query])).astype('float32')

    distances, indices = index.search(query_embedding, k=3)

    print("\nTop Matches:\n")
    for i, idx in enumerate(indices[0]):
        print(f"{i+1}. {documents[idx]}")
        print(f"Distance: {distances[0][i]}\n")
