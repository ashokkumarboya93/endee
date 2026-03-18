import requests, json

# Test search endpoint
print("Testing /search endpoint...")
r = requests.post('http://localhost:8000/search', json={
    'error_string': 'IndexError: list index out of range',
    'language': 'Python',
    'top_k': 3
})
print(f"Status: {r.status_code}")
data = r.json()
results = data.get('results', [])
print(f"Results: {len(results)}")
for x in results:
    print(f"  {x['error'][:60]} | Score: {x['score']:.2f} | Lang: {x['language']}")

print("\nTesting /rag endpoint...")
if results:
    r2 = requests.post('http://localhost:8000/rag', json={
        'error_string': 'IndexError: list index out of range',
        'language': 'Python',
        'retrieved_contexts': results
    })
    print(f"Status: {r2.status_code}")
    if r2.ok:
        print(f"AI explanation length: {len(r2.json().get('explanation', ''))}")
    else:
        print(f"Error: {r2.text[:200]}")
