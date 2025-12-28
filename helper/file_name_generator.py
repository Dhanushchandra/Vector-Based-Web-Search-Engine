from urllib.parse import urlparse
from datetime import datetime
import os

def generate_index_path(seed_url):
    domain = urlparse(seed_url).netloc.replace(".", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"data/{domain}_{timestamp}.json"