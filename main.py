from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Initialize OpenAI client (uses OPENAI_API_KEY from env)
client = OpenAI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

def scrape_islamqa(query: str) -> str:
    url = f"https://islamqa.info/en/search?query={query.replace(' ', '+')}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select("a.block.py-4.border-b")
    if not links:
        return "No fatwa found."
    top_link = "https://islamqa.info" + links[0]['href']
    article = requests.get(top_link)
    content = BeautifulSoup(article.text, "html.parser").select("div.answercontent p")
    return "\n".join(p.text for p in content[:4])  # First 4 paragraphs

@app.post("/ask")
async def ask(data: Question):
    query = data.question
    scraped = scrape_islamqa(query)

    prompt = (
        f"A Muslim user asked: '{query}'.\n\n"
        f"Here is an answer from IslamQA:\n{scraped}\n\n"
        f"Please do two things:\n"
        f"1. **Summarize the key points from the IslamQA answer** (if available) using bullet points and line breaks.\n"
        f"2. **Provide a clear, concise, and respectful Islamic answer** in your own words, based on Qur'an, Hadith, and scholarly consensus.\n"
        f"- Format the final answer clearly with bold text for titles or important terms.\n"
        f"- Use emojis sparingly to make sections visually engaging, e.g., 📿 for prayer, 📖 for Quran, 🙏 for supplication.\n"
        f"- Make the content well-spaced and easy to read."
    )


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Islamic assistant. Your advice should be based on Qur'an, Hadith, and scholarly consensus."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"answer": response.choices[0].message.content}
