import json
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def generate_index_path(seed_url):
    domain = urlparse(seed_url).netloc.replace(".", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"data/{domain}_{timestamp}.json"

def build_embeddings(pages, output_path):
    records = []

    for page in pages:
        text = f"{page['title']}\n\n{page['content']}"
        embedding = model.encode(text).tolist()

        records.append({
            "url": page["url"],
            "title": page["title"],
            "embedding": embedding
        })

        with open(output_path, "w") as f:
            json.dump(records, f)

        print(f"Saved {len(records)} embeddings")