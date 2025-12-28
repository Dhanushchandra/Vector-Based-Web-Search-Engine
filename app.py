from flask import Flask, request, jsonify
from crawler.crawl import crawl
from search.embed import build_embeddings
from search.semantic_search import search

app = Flask(__name__)

@app.route("/crawl", methods=["POST"])
def crawl_state():
    url = request.json.get("url")
    pages = crawl(url)
    build_embeddings(pages)
    return jsonify({"message": "Crawling & indexing completed", "pages": len(pages)})

@app.route("/search", methods=["GET"])
def search_query():
    query = request.args.get("q")
    results = search(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)