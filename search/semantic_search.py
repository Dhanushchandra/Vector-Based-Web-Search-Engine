import json
import torch
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"
DATA_PATH = "data/embeddings.json"

model = SentenceTransformer(MODEL_NAME)

with open(DATA_PATH, "r") as f:
    records = json.load(f)

embeddings = torch.tensor([r["embedding"] for r in records])

def search(query, top_k=2):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, embeddings)[0]

    top_results = torch.topk(scores, k=top_k)

    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        results.append({
            "title": records[idx]["title"],
            "url": records[idx]["url"],
            "score": float(score)
        })

    return results


results = search("car")

print(results)