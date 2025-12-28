import requests
from collections import deque
from extract import extract_text_and_links

HEADERS = {"User-Agent": "VectorWebSearhBot/1.0"}
MAX_PAGES = 20
MAX_DEPTH = 2

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
        print(f"Crawling: {url}")

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

pages = crawl("https://en.wikipedia.org/wiki/Main_Page")

print(pages)