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

@app.route("/delete-embedding", methods=["DELETE"])
def delete_embedding():
    index_path = request.args.get("index_path")

    if not index_path:
        return jsonify({"error": "index_path is required"}), 400

    if not index_path.endswith(".json"):
        index_path = f"{index_path}.json"
    print(index_path)
    full_path = os.path.join("data", index_path)

    if not os.path.exists(full_path):
        return jsonify({"error": "Index file not found"}), 404

    try:
        os.remove(full_path)
    except Exception as e:
        return jsonify({
            "error": "Failed to delete index",
            "details": str(e)
        }), 500

    return jsonify({
        "message": "Index deleted successfully",
        "index": index_path
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)