# Vector-Based Semantic Website Search Engine

🔗 **Live Demo:** https://vector.dolab.in  

A semantic web search engine that crawls websites, generates vector embeddings, and enables **meaning-based search** instead of traditional keyword matching.

---

## 🚀 Overview

Traditional search engines rely on exact keyword matches, which often fail to capture user intent.  
This project demonstrates how **vector embeddings + similarity search** can be used to build a smarter search system that understands context and semantics.

Example:  
Searching for *“feline”* can still retrieve pages that mention *“cat”*.

---

## ✨ Features

- 🌐 Website crawling and content extraction  
- 🧠 Semantic embeddings using Sentence Transformers  
- 📐 Cosine similarity–based search  
- 📂 Multiple crawl indexes (search within a specific crawl)  
- 🔍 Search results ranked by semantic relevance  
- 🖥️ Simple web UI + REST APIs  
- ☁️ Deployed on AWS EC2 (Amazon Linux)

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **ML / NLP:** Sentence Transformers, PyTorch  
- **Search:** Vector embeddings + Cosine similarity  
- **Web Crawling:** Requests, BeautifulSoup  
- **Deployment:** AWS EC2 (Amazon Linux)  

---

## 🔍 How It Works

1. **Crawl**  
   The crawler visits pages starting from a seed URL and extracts clean, visible text.

2. **Embed**  
   Each page’s content is converted into a high-dimensional vector using a transformer-based embedding model.

3. **Store**  
   Embeddings are stored per crawl index for isolated searching.

4. **Search**  
   User queries are embedded and compared against stored vectors using cosine similarity to find the most relevant pages.

---

## 🧠 Key Learnings

- Embeddings enable search by **meaning**, not just keywords  
- Retrieval quality often matters more than model size  
- ML systems fail in practice due to **infrastructure constraints**, not algorithms  
- Dependency management, memory limits, and disk space are real challenges in production ML  

---

## ⚠️ Limitations & Future Improvements

- Replace JSON storage with a vector database (FAISS / Chroma)
- Add chunk-level indexing for better recall
- Introduce RAG-style answers with source citations
- Improve crawler robustness (robots.txt, rate limiting)

---

## 📌 Live Demo

👉 **https://vector.dolab.in**

---

## 📄 License

This project is for educational and demonstration purposes.

---

## 🙌 Author

Built by **Dhanush**  
Feel free to explore, fork, or reach out for collaboration.
