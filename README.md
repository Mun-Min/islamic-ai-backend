# 🕌 Islamic AI Backend

This is the backend API for the Islamic AI Q&A application, built with **FastAPI** and hosted on **Render**. It uses the **OpenAI API** to generate Islamic answers based on user questions.

---

## 📦 Tech Stack

- **Python 3.11**
- **FastAPI**
- **OpenAI API**
- **BeautifulSoup4** (optional for web scraping)
- **Render** for deployment
- **CORS** for frontend/backend communication

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.11+
- An OpenAI API Key
- (Optional) Render.com account for deployment

### 🔑 Environment Variables

Create a `.env` file with the following:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 📥 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/Mun-Min/islamic-ai-backend.git
cd islamic-ai-backend
pip install -r requirements.txt
```

### ▶️ Run Locally

```bash
uvicorn main:app --reload
```

---

## 🔁 API Usage

### 📩 POST `/ask`

Send a question to receive an Islamic AI-generated answer.

#### Request Body

```json
{
  "question": "How to pray the daily prayers?"
}
```

#### Response

```json
{
  "answer": "🕌 Here are the steps to perform daily prayers..."
}
```

---

## 🌐 Deployment (Render)

1. Create a new Web Service on Render.
2. Connect your GitHub repo.
3. Set the build command (optional): `pip install -r requirements.txt`
4. Set the start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Add `OPENAI_API_KEY` in the Render environment variables.

---

## 📁 Project Structure

```
.
├── main.py            # FastAPI app
├── requirements.txt   # Python dependencies
└── .env               # Environment variables (not committed)
```

---

## ⚠️ Disclaimer

This API generates Islamic content using AI. While it aims to provide guidance based on authentic sources, please consult qualified scholars for religious decisions.

---

## 📜 License

MIT License