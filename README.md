🚀 FinQuest-AI

FinQuest-AI is a FastAPI-based Retrieval-Augmented Generation (RAG) project designed for financial document analysis. This branch uses Qdrant as the vector database to store and search embeddings.

---

🛠️ Project Setup

🔁 Clone the Repository

```bash
git clone -b RAG-quadrant https://github.com/pintuprajapati/FinQuest-AI.git
cd FinQuest-AI
```

---

💡 Environment Setup

🔹 Create and Activate Virtual Environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

🔐 Environment Variables

1. Copy the .env.sample file and rename it to .env:

```bash
cp .env.sample .env
```

2. Fill in the necessary values inside .env as needed (e.g., API keys, Qdrant URL, etc.).

---

🧠 Qdrant Setup (Vector DB)

Make sure you have Docker installed and running on your machine.

🔹 Pull the latest Qdrant image:

```bash
docker pull qdrant/qdrant
```

🔹 Run Qdrant locally:

On Windows (CMD/PowerShell):

```bash
docker run -p 6333:6333 -p 6334:6334 ^
    -v "%cd%/qdrant_storage:/qdrant/storage:z" ^
    qdrant/qdrant
```

On Linux/macOS:

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

🔹 Qdrant will be accessible at:
- REST API: http://localhost:6333
- Dashboard: http://localhost:6333/dashboard
- gRPC API: localhost:6334

---

🚀 Run the FastAPI Server

```bash
python main.py
```

Your FastAPI app should now be running on:

```
http://127.0.0.1:8000
```


---

📬 API Docs

FastAPI automatically provides interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

✨ Author

Pintu Rajpati  
Feel free to connect or contribute!

---

