from endee import Endee
client = Endee()
index_name = "debugbot_errors"
try:
    client.delete_index(index_name)
    print(f"Deleted index {index_name}")
except Exception as e:
    print(f"Index might not exist: {e}")
