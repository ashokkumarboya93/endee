from endee import Endee
client = Endee()
try:
    indices = client.list_indexes()
    print(f"Indices: {indices}")
except Exception as e:
    print(f"Failed to list indices: {e}")
