from sentence_transformers import SentenceTransformer
from endee import Endee
import json

e = SentenceTransformer('all-MiniLM-L6-v2')
text = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
vec = e.encode([text])[0].tolist()

client = Endee()
index = client.get_index("debugbot_errors")

res = index.query(vec, top_k=10)
for r in res:
    print(f"ID: {r.get('id')} | Similarity: {r.get('similarity'):.4f} | Lang: {r['meta'].get('language')}")
