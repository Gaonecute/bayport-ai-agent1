from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import httpx
import uvicorn

app = FastAPI()

# Simulated CRM integration (Vtiger CRM API)
VTIGER_API_URL = "https://example.vtigercrm.com/api"
VTIGER_API_KEY = "your_api_key_here"

# AI Agent prompts
BASE_PROMPT = """
You are BayportBot, a helpful and friendly AI assistant for Bayport Botswana. You help users with:
- Downloading statements 📑
- Booking settlements 📅
- Requesting a callback 📞
- Understanding loan products and services
- Performing loan calculations
You must respond concisely and accurately, guiding users step-by-step.
"""

class UserQuery(BaseModel):
    message: str
    user_id: Optional[str] = None

async def query_openai(prompt: str) -> str:
    # Call to OpenAI (replace with real API key and endpoint if needed)
    headers = {"Authorization": f"Bearer your_openai_key"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": BASE_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            headers=headers
        )
    result = response.json()
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    return "I'm sorry, I couldn't generate a response at the moment."

@app.post("/chat")
async def chat_with_user(user_query: UserQuery):
    user_message = user_query.message
    response = await query_openai(user_message)
    return {"response": response}

@app.post("/request-callback")
async def request_callback(data: dict):
    # Simulated Vtiger CRM API call to create a call-back request
    payload = {
        "api_key": VTIGER_API_KEY,
        "module": "Leads",
        "action": "create_callback",
        "data": data
    }
    async with httpx.AsyncClient() as client:
        crm_response = await client.post(f"{VTIGER_API_URL}/callback", json=payload)
    return crm_response.json()

@app.get("/download-statement")
async def download_statement(user_id: str):
    # Placeholder: Pull from user database or CRM
    return {"message": f"Statement for user {user_id} downloaded successfully."}

@app.post("/book-settlement")
async def book_settlement(data: dict):
    # Placeholder for settlement booking logic
    return {"message": "Settlement successfully booked.", "details": data}

# Use this to run with: uvicorn bayport_ai_agent:app --host 0.0.0.0 --port 8000 --reload
# Only run this line manually from terminal, not from inside the script.
