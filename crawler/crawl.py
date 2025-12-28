import requests
import json
from collections import deque
from .extract import extract_text_and_links
from search.embed import build_embeddings

HEADERS = {"User-Agent": "VectorWebSearhBot/1.0"}
MAX_PAGES = 20
MAX_DEPTH = 2
OUTPUT_FILE = "crawled_pages.json"

def crawl(seed_url):
    visited = set()
    queue = deque([(seed_url,0)])
    pages = []

    print(queue)

    while queue and len(pages) < MAX_PAGES:
        url, depth = queue.popleft()

        if url in visited or depth > MAX_DEPTH:
            continue

        visited.add(url)
        print(f"Crawling ({len(pages)+1}/{MAX_PAGES}): {url}")

        try:
            res = requests.get(url,headers=HEADERS,timeout=10)
            res.raise_for_status()
        except Exception as e:
            print("Failed:",e)
            continue

        title, content, links = extract_text_and_links(res.text, seed_url)

        pages.append({
                "url": url,
                "title": title,
                "content": content
            })
    

    
        for link in links:
                if link not in visited:
                    queue.append((link, depth + 1))

    return pages

# --- Execution ---
seed = "https://en.wikipedia.org/wiki/Main_Page"
scraped_data = crawl(seed)

build_embeddings(scraped_data)

# Saving to JSON
# try:
#     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#         # indent=4 makes the file human-readable
#         # ensure_ascii=False handles non-English characters correctly
#         json.dump(scraped_data, f, indent=4, ensure_ascii=False)
#     print(f"\nSuccessfully saved {len(scraped_data)} pages to {OUTPUT_FILE}")
# except Exception as e:
#     print(f"Error saving file: {e}")