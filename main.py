from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Request
from typing import List, Optional
import uvicorn
import random
import string
import httpx

import requests
import sys
from ollama_pdf_chat import agent


app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
async def root():
    return {"message": "Hello World"}
  
@app.get("/random_string")
async def get_random_string(length: int = 10):
    """
    Generate a random string of fixed length
    """
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return {"random_string": letters}

@app.post("/get_prompt_response")
async def get_prompt_response(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    url = "http://127.0.0.1:11434/api/generate"
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            url,
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False
            }
        )

    return response.json()

@app.post("/ollama_pdf_chat")
async def ollama_pdf_chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    return {"message": "Ollama PDF chat response", "response": prompt}

