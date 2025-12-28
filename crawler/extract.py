from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_text_and_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title else ""

    text = " ".join(
        chunk.strip()
        for chunk in soup.get_text(separator=" ").split()
        if chunk.strip()
    )

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#")[0]
        link = urljoin(base_url, href)

        if urlparse(link).netloc == urlparse(base_url).netloc:
            links.add(link)

    return title, text, links
