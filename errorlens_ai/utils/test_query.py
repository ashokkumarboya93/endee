from endee import Endee
from sentence_transformers import SentenceTransformer

def test_query():
    print("Connecting to Endee...")
    client = Endee()
    index = client.get_index("debugbot_errors")
    
    print("Loading model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    query = "TypeError: object is not a function"
    print(f"Querying: {query}")
    vector = model.encode([query])[0].tolist()
    
    results = index.query(vector=vector, top_k=2)
    print(f"Found {len(results)} results:")
    for res in results:
        # Check if it has meta attribute or if it's a dict
        if hasattr(res, 'meta'):
             print(f" - [{res.similarity:.2f}] {res.meta.get('error', 'no error')}")
        else:
             print(f" - Result: {res}")

if __name__ == "__main__":
    test_query()
