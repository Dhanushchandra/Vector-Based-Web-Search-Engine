import json
import os
from flask import Flask, request, jsonify
from crawler.crawl import crawl
from search.embed import build_embeddings
from search.semantic_search import search
from helper.file_name_generator import generate_index_path
from helper.meta_data_functions import get_all_embeddings_names, get_embedding_links_and_title

app = Flask(__name__)

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
    files = get_all_embeddings_names()

    return jsonify({
        "indexes": files
    })

@app.route("/get-embedding-links", methods=["GET"])
def get_embedding_links():
    index_path = request.args.get("index_path")
    meta_data = get_embedding_links_and_title(index_path)

    return meta_data

if __name__ == "__main__":
    app.run(debug=True)