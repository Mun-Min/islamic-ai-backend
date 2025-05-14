from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from typing import List, Literal
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Initialize OpenAI client (uses OPENAI_API_KEY from env)
client = OpenAI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/ask")
async def ask(data: ChatRequest):
    # Add a system instruction at the start of the message list
    system_message = {
        "role": "system",
        "content": (
            "You are a helpful Islamic assistant. Answer questions based only on the Qur'an, Hadith, and scholarly consensus. "
            "Only respond to Islamic-related questions. Politely decline or redirect if the question is unrelated to Islam. "
            "Format answers clearly with bold titles where appropriate, use sparse emojis like 📿 or 📖, and ensure clarity and Islamic decorum."
            "Do not create excessive line spacing."
        )
    }

   # Combine system message with user chat history
    full_messages = [system_message] + [msg.model_dump() for msg in data.messages]

    # Send to OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=full_messages
    )

    return {"answer": response.choices[0].message.content.strip()}