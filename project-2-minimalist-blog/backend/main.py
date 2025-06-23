from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORS

app = FastAPI()

# Enable CORS to allow frontend communication
app.add_middleware(
    CORS,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Updated Post model with author, date, and category
class PostFull(BaseModel):
    id: int
    title: str
    content: str  # Now stores Markdown content
    author: str
    date: str
    category: str

# Fake database with sample posts including new fields
fake_posts_db = [
    {
        "id": 1,
        "title": "First Post",
        "content": "# Welcome\nThis is the **first post** in Markdown format.\n\n- Point 1\n- Point 2",
        "author": "John Doe",
        "date": "2025-06-23",
        "category": "Tech"
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "## News Update\nThis is another post written in **Markdown**.\n\n[Visit xAI](https://x.ai)",
        "author": "Jane Smith",
        "date": "2025-06-22",
        "category": "News"
    }
]

@app.get("/posts/", response_model=List[PostFull])
async def get_posts():
    return fake_posts_db

@app.get("/posts/{post_id}", response_model=PostFull)
async def get_post(post_id: int):
    for post in fake_posts_db:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")