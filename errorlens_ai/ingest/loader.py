import os
import traceback
import pandas as pd
from sentence_transformers import SentenceTransformer
from endee import Endee, Precision

def ingest_data():
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Connecting to Endee Vector Database...")
    client = Endee()

    index_name = "debugbot_errors"
    try:
        # Create index if it does not exist
        client.create_index(
            name=index_name,
            dimension=384,
            space_type="cosine",
            precision=Precision.INT8
        )
        print(f"Created index: {index_name}")
    except Exception as e:
        print(f"Index creation output (might already exist): {e}")

    index = client.get_index(name=index_name)

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    csv_files = ["python_errors.csv", "java_errors.csv", "javascript_errors.csv", "sql_errors.csv"]

    all_vectors = []
    
    # Process each CSV
    for filename in csv_files:
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}. Skipping.")
            continue
            
        print(f"Processing {filename}...")
        df = pd.read_csv(filepath)
        
        # Verify required columns exist
        required_cols = ['error', 'solution', 'language', 'context']
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            print(f"Missing columns {missing_cols} in {filename}. Skipping.")
            continue
            
        errors = df['error'].astype(str).tolist()
        print(f"  Computing embeddings for {len(errors)} errors...")
        embeddings = model.encode(errors, convert_to_numpy=True)
        
        print("  Formatting for Endee...")
        for i, row in df.iterrows():
            doc_id = f"{filename.split('_')[0]}_{i}"
            meta = {
                "error": str(row['error']),
                "solution": str(row['solution']),
                "language": str(row['language']),
                "context": str(row['context'])
            }
            vector_item = {
                "id": doc_id,
                "vector": embeddings[i].tolist(),
                "meta": meta,
                "filter": {"language": str(row['language'])}
            }
            all_vectors.append(vector_item)

    if not all_vectors:
        print("No data to insert.")
        return

    print(f"Upserting {len(all_vectors)} total items into Endee...")
    
    # Batch the upsert in chunks of 500 to avoid memory / payload size issues
    chunk_size = 300
    for i in range(0, len(all_vectors), chunk_size):
        batch = all_vectors[i:i+chunk_size]
        try:
            index.upsert(batch)
            print(f"Inserted batch {i//chunk_size + 1} ({len(batch)} items). First ID: {batch[0]['id']}")
        except Exception as e:
            print(f"Failed to upsert batch {i//chunk_size + 1}: {e}")

    print("Data ingestion complete!")

if __name__ == "__main__":
    try:
        ingest_data()
    except Exception:
        traceback.print_exc()
