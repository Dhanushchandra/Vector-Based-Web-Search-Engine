import os
import json
from flask import Flask, request, jsonify


DATA_DIR = "data"


import os

def get_all_embeddings_names():
    # Only return the name part of the file
    files = [
        f.replace(".json", "") 
        for f in os.listdir(DATA_DIR) 
        if f.endswith(".json")
    ]
    return files


def get_embedding_links_and_title(index_name):
    if not index_name:
        return jsonify({"error": "index_path is required"}), 400

    full_path = os.path.join("data", f"{index_name}.json")

    if not os.path.exists(full_path):
        return jsonify({"error": "Index file not found"}), 404

    with open(full_path, "r") as f:
        records = json.load(f)

    links = [
        {
            "title": r["title"],
            "url": r["url"]
        }
        for r in records
    ]

    return jsonify({
        "count": len(links),
        "links": links
    })
