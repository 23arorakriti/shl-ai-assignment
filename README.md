# SHL Assessment Recommendation Agent

An AI-powered assessment recommendation system that helps recruiters identify the most suitable SHL assessments based on job descriptions, required skills, experience levels, and hiring needs. The application combines semantic search using FAISS with Retrieval-Augmented Generation (RAG) powered by Google's Gemini model to deliver accurate and contextual recommendations through a conversational interface.

---

## 🚀 Live Demo

- **Frontend (Streamlit):** https://shl-ai-assignment.streamlit.app/
- **API Documentation/Backend Review:** https://panda0987-shl-project.hf.space/docs
- **Backend version test:** https://panda0987-shl-project.hf.space

---

## ✨ Features

- 🤖 AI-powered SHL assessment recommendations
- 🔍 Semantic search using FAISS vector database
- 🧠 Retrieval-Augmented Generation (RAG)
- 💬 Conversational recommendation interface
- 📋 Context-aware multi-turn conversations
- 🛡️ Prompt injection protection
- 🚫 Out-of-scope query detection
- ⚡ FastAPI REST API backend
- 🎨 Streamlit frontend
- ☁️ Cloud deployment using Hugging Face Spaces and Streamlit Community Cloud

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Uvicorn
- LangChain
- Google Gemini 2.5 Flash
- FAISS
- HuggingFace Embeddings
- Pydantic

### Frontend
- Streamlit
- Requests

### AI & Retrieval
- Google Gemini 2.5 Flash
- sentence-transformers/all-MiniLM-L6-v2
- FAISS Vector Store

---

## 📂 Project Structure

```text
.
├── data/
│   └── shl_product_catalog.json
├── ingestion/
│   └── build_index.py
├── prompts/
│   └── system_prompt.txt
├── retrieval/
│   └── retriever.py
├── utils/
│   └── rules.py
├── app.py
├── streamlit_app.py
├── config.py
├── models.py
├── requirements-api.txt
├── Dockerfile
└── README.md
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API status |
| GET | `/health` | Health check |
| POST | `/chat` | Get assessment recommendations |
| GET | `/docs` | Interactive Swagger documentation |

---

## 💡 Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Recommend assessments for a Senior Java Backend Developer with Spring Boot, SQL, Docker and AWS."
    }
  ]
}
```

---

## 💡 Example Response

```json
{
  "reply": "Based on your requirements, I recommend the following SHL assessments...",
  "recommendations": [
    {
      "name": "Java Assessment",
      "url": "https://www.shl.com/...",
      "test_type": "Knowledge & Skills"
    }
  ],
  "end_of_conversation": false
}
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd SHL_Project
```

### 2. Install dependencies

```bash
pip install -r requirements-api.txt
```

### 3. Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### 4. Build the vector database

```bash
python ingestion/build_index.py
```

### 5. Run the FastAPI backend

```bash
uvicorn app:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

### 6. Run the Streamlit frontend

```bash
streamlit run streamlit_app.py
```

---

## ☁️ Deployment

### Backend
- Hugging Face Spaces (Docker)
- FastAPI
- Automatic FAISS index generation during Docker build

### Frontend
- Streamlit Community Cloud
- Communicates with the deployed FastAPI backend using REST APIs

---

## 🔒 Security Features

- Prompt injection protection
- Out-of-scope query detection
- Input validation using Pydantic
- Controlled recommendation generation
- Safe conversational context handling

---

## 📜 License

This project was developed as part of the **SHL AI Assessment Recommendation Assignment** and is intended for educational and evaluation purposes.

---

## 👩‍💻 Author

**Kriti Arora**

- GitHub: https://github.com/23arorakriti
