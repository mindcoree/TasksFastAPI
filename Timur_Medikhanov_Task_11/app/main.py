from fastapi import FastAPI
from pydantic import BaseModel
from .tasks import send_email_simulation

app = FastAPI()

class Email(BaseModel):
    recipient: str
    message: str


@app.post("/send-email")
async def send_email(email: Email):
    task = send_email_simulation.delay(email.recipient,email.message)
    return {"task_id":task.id,"status":"Email task queued"}


