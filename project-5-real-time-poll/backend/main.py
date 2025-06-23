import os
import json
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

# --- Настройка CORS ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Работа с polls.json ---
POLL_FILE = "polls.json"

def load_polls():
    if os.path.exists(POLL_FILE):
        with open(POLL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_polls():
    with open(POLL_FILE, "w", encoding="utf-8") as f:
        json.dump(polls, f, ensure_ascii=False, indent=2)

# --- "База данных" в памяти ---
polls: List[dict] = load_polls()

# --- Pydantic модели ---
class PollCreateRequest(BaseModel):
    question: str
    options: List[str]

class PollResponse(BaseModel):
    id: str
    question: str
    options: Dict[str, Dict[str, int | str]]

# --- Эндпоинты API ---

@app.get("/api/poll", response_model=List[PollResponse])
async def get_polls():
    """Возвращает все опросы."""
    return polls

@app.get("/api/poll/{poll_id}", response_model=PollResponse)
async def get_poll(poll_id: str):
    for poll in polls:
        if poll["id"] == poll_id:
            return poll
    raise HTTPException(status_code=404, detail="Poll not found")

@app.post("/api/poll/create", response_model=PollResponse)
async def create_poll(req: PollCreateRequest):
    poll_id = str(uuid4())
    options = {k: {"label": k, "votes": 0} for k in req.options}
    poll = {"id": poll_id, "question": req.question, "options": options}
    polls.append(poll)
    save_polls()
    return poll

@app.post("/api/poll/vote/{poll_id}/{option_key}", response_model=PollResponse)
async def cast_vote(poll_id: str, option_key: str):
    for poll in polls:
        if poll["id"] == poll_id:
            if option_key not in poll["options"]:
                raise HTTPException(status_code=404, detail="Option not found")
            poll["options"][option_key]["votes"] += 1
            save_polls()
            return poll
    raise HTTPException(status_code=404, detail="Poll not found")
