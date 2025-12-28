from flask import Flask, request, jsonify
from crawler.crawl import crawl
from search.embed import build_embeddings
from search.semantic_search import search
from urllib.parse import urlparse
from datetime import datetime
import os

app = Flask(__name__)

def generate_index_path(seed_url):
    domain = urlparse(seed_url).netloc.replace(".", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"data/{domain}_{timestamp}.json"

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

if __name__ == "__main__":
    app.run(debug=True)