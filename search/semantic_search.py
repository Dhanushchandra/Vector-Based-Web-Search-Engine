import json
import torch
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def load_index(index_path):
    with open(f"data/{index_path}.json", "r") as f:
        records = json.load(f)

    embeddings = torch.tensor([r["embedding"] for r in records])
    return records, embeddings

def search(query,index_path, top_k=2):
    records, embeddings = load_index(index_path)

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
