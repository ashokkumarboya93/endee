from endee import Endee
client = Endee()
index = client.get_index("debugbot_errors")
print("Attempting query with filter...")
try:
    res = index.query(vector=[0.1]*384, top_k=5, filter=[{"language": {"$eq": "Python"}}])
    print(f"Success! Found {len(res)} results.")
    for r in res:
        print(f"ID: {r.get('id')} Meta Lang: {r['meta'].get('language')}")
except Exception as e:
    print(f"Failed: {e}")
