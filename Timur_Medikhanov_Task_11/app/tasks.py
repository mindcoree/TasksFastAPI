from .celery_config import app
import time

@app.task
def send_email_simulation(recipient:str,message:str):
    print(f"Sending email to {recipient}")
    time.sleep(5)
    print(f"Email sent to {recipient} with message {message}")
    return {
        "status": "success",
        "recipient": recipient,
    }