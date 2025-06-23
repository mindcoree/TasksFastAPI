import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# --- App Configuration ---
app = FastAPI()

# --- CORS Configuration ---
# This allows your Next.js frontend (running on http://localhost:3000)
# to communicate with your FastAPI backend.
origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)


# --- Pydantic Models (Data Shape) ---
class TodoItem(BaseModel):
    id: str
    task: str
    completed: bool = False

class TodoCreate(BaseModel):
    task: str # Only need the task text to create a new todo

class TodoUpdate(TodoCreate):
    pass

# --- In-Memory Database (a simple Python list) ---
# This list will act as our database. It will reset when the server restarts.
fake_todo_db: List[TodoItem] = []


# --- API Endpoints ---

@app.get("/api/todos", response_model=List[TodoItem])
async def get_all_todos():
    """Returns all items in the to-do list."""
    return fake_todo_db

@app.post("/api/todos", response_model=TodoItem, status_code=201)
async def create_todo(todo_data: TodoCreate):
    """Creates a new to-do item."""
    new_todo = TodoItem(
        id=str(uuid.uuid4()), # Generate a unique ID
        task=todo_data.task,
        completed=False
    )
    fake_todo_db.append(new_todo)
    return new_todo

@app.put("/api/todos/{todo_id}")
async def update_todo(todo_id:str,todo_data:TodoUpdate) -> TodoItem:
    new_todo = TodoItem(
        id=str(uuid.uuid4()),
        task=todo_data.task,
        completed=False,
    )
    fake_todo_db.append(new_todo)
    return new_todo

@app.patch("/api/todos/{todo_id}", response_model=TodoItem)
async def update_todo_status(todo_id: str):
    """Toggles the 'completed' status of a to-do item."""
    for todo in fake_todo_db:
        if todo.id == todo_id:
            todo.completed = not todo.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/api/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: str):
    """Deletes a to-do item."""
    todo_to_delete = None
    for todo in fake_todo_db:
        if todo.id == todo_id:
            todo_to_delete = todo
            break
    if not todo_to_delete:
        raise HTTPException(status_code=404, detail="Todo not found")

    fake_todo_db.remove(todo_to_delete)
    # No content is returned for a 204 response
    return

@app.delete("/app/todos/completed",status_code=204)
async def delete_todo():
    global fake_todo_db
    take_todo_db = [todo for todo in fake_todo_db if not todo.completed]
    return

# A simple root endpoint to confirm the server is running
@app.get("/")
async def root():
    return {"message": "FastAPI To-Do Backend is running!"}