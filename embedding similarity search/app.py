from search import search

def main():
    print("🔍 Semantic Search System (FAISS)")
    
    while True:
        query = input("\nEnter query (or 'exit'): ")
        
        if query.lower() == "exit":
            print("Exiting...")
            break
        
        results = search(query)
        
        print("\nTop Results:")
        for r in results:
            print(f"- {r['text']} (score: {r['score']:.4f})")

if __name__ == "__main__":
    main()