import json
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
DATA_PATH = "data/embeddings.json"

model = SentenceTransformer(MODEL_NAME)

def build_embeddings(pages):
    records = []

    for page in pages:
        text = f"{page['title']}\n\n{page['content']}"
        embedding = model.encode(text).tolist()

        records.append({
            "url": page["url"],
            "title": page["title"],
            "embedding": embedding
        })

        with open(DATA_PATH, "w") as f:
            json.dump(records, f)

        print(f"Saved {len(records)} embeddings")