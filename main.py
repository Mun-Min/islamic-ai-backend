from fastapi import FastAPI
from pydantic import BaseModel
import openai
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use Netlify domain in production
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
    return "\n".join(p.text for p in content[:4])  # Get 4 paragraphs

@app.post("/ask")
async def ask(data: Question):
    query = data.question
    scraped = scrape_islamqa(query)

    prompt = (
        f"A Muslim user asked: '{query}'.\n\n"
        f"Here is an answer from IslamQA:\n{scraped}\n\n"
        f"Please do two things:\n"
        f"1. Summarize the key points from the IslamQA answer.\n"
        f"2. Then provide a well-rounded response in your own words, based on authentic Islamic sources "
        f"and your understanding as a knowledgeable assistant.\n"
        f"Make sure the final response is clear and respectful."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful Islamic assistant. Your advice should be based on Qur'an, Hadith, and scholarly consensus."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"answer": response["choices"][0]["message"]["content"]}

