from endee import Endee
client = Endee()
index = client.get_index("debugbot_errors")

# Try to get python_0 meta
try:
    # Endee might not have a direct 'get' by ID in the same way, but we can try to find what's there
    # Let's try to query for things that definitely should be Python
    # Or just list some IDs if possible. Since we can't 'list', we'll query with a dummy vector and high top_k
    res = index.query([0.1]*384, top_k=512)
    langs = [r['meta'].get('language') for r in res]
    from collections import Counter
    print(Counter(langs))
except Exception as e:
    print(f"Error: {e}")
