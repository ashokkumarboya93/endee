from sentence_transformers import SentenceTransformer
from endee import Endee
e = SentenceTransformer('all-MiniLM-L6-v2')
vec = e.encode(["TypeError: unsupported operand type(s) for +: 'int' and 'str'"])[0].tolist()
res = Endee().get_index('debugbot_errors').query(vec, top_k=5)
for r in res:
    print(r.get('id'), r['meta'].get('language'))
