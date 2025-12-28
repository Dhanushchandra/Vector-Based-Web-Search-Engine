import json
import os
from flask import Flask, request, jsonify
from crawler.crawl import crawl
from search.embed import build_embeddings
from search.semantic_search import search
from helper.file_name_generator import generate_index_path

app = Flask(__name__)

DATA_DIR = "data"

@app.route("/crawl", methods=["POST"])
def crawl_state():
    url = request.json.get("url")
    pages = crawl(url)
    index_path = generate_index_path(url)
    build_embeddings(pages,index_path)
    return jsonify({"message": "Crawling & indexing completed", "pages": len(pages),"index": index_path},)

@app.route("/search", methods=["GET"])
def search_query():
    query = request.args.get("q")
    index_path = request.args.get("index_path")
    results = search(query,index_path)
    return jsonify(results)

@app.route("/get-all-embeddings", methods=["GET"])
def get_all_embeddings():
    files = [
        f for f in os.listdir(DATA_DIR)
        if f.endswith(".json")
    ]

    return jsonify({
        "indexes": files
    })

@app.route("/get-embedding-links", methods=["GET"])
def get_embedding_links():
    index_path = request.args.get("index_path")

    if not index_path:
        return jsonify({"error": "index_path is required"}), 400

    full_path = os.path.join("data", index_path)

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

if __name__ == "__main__":
    app.run(debug=True)