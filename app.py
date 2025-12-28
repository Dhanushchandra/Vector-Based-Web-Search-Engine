import json
import os
from flask import Flask, request, jsonify, render_template
from crawler.crawl import crawl
from search.embed import build_embeddings
from search.semantic_search import search
from helper.file_name_generator import generate_index_path
from helper.meta_data_functions import get_all_embeddings_names, get_embedding_links_and_title

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/crawl", methods=["POST"])
def crawl_state():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "url is required"}), 400

    url = data["url"]

    try:
        pages = crawl(url)
    except Exception as e:
        return jsonify({
            "error": "Crawling failed",
            "details": str(e)
        }), 500

    if not pages:
        return jsonify({
            "message": "Crawling completed but no indexable pages found",
            "pages": 0
        }), 200

    index_path = generate_index_path(url)

    try:
        build_embeddings(pages, index_path)
    except Exception as e:
        return jsonify({
            "error": "Embedding generation failed",
            "details": str(e)
        }), 500

    return jsonify({
        "message": "Crawling & indexing completed",
        "pages": len(pages),
        "index": index_path.split("/")[-1]
    }), 200


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