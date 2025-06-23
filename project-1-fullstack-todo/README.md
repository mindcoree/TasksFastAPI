# Project 1/10: Full-Stack To-Do List

This is a minimal yet complete full-stack web application featuring a **Next.js** frontend and a **FastAPI** backend. It serves as a practical, hands-on template for understanding modern web development architecture.

![App Screenshot](https://i.imgur.com/your-screenshot-url.png) ---

## 🚀 Tech Stack

* **Frontend:** [Next.js](https://nextjs.org/) (with React, TypeScript, and Tailwind CSS)
* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python asynchronous framework)
* **Package Manager:** [PNPM](https://pnpm.io/)
* **Database:** In-memory Python list (resets on server restart)

---

## ✨ Features

* **Create:** Add new tasks to the list.
* **Read:** View all current tasks.
* **Update:** Mark tasks as 'completed' by clicking on them.
* **Delete:** Remove tasks from the list.
* **CORS Enabled:** Backend is configured to accept requests from the frontend.

---

## 🎓 Task for Students & Learners

Your challenge is to clone this project and extend its functionality. This is a great way to practice your skills.

### Your Mission:

1.  **Clone & Run:**
    * Clone this repository to your local machine.
    * Follow the setup steps below to get both the frontend and backend running.

2.  **Add an "Edit" Feature:**
    * **Backend:** Create a new `PUT /api/todos/{todo_id}` endpoint in `backend/main.py` that allows changing the text of an existing task.
    * **Frontend:** Add an "Edit" button next to each task. When clicked, it should allow the user to modify the task's text and save the changes by calling your new backend endpoint.

3.  **Add a "Clear All Completed" Button:**
    * **Backend:** Implement a `DELETE /api/todos/completed` endpoint that removes all tasks marked as complete.
    * **Frontend:** Add a button that calls this new endpoint to clear multiple tasks at once.

4.  **Improve Styling:**
    * Get creative! Change the colors, fonts, and layout. Add animations or transitions to make the user experience smoother.

---

## ⚙️ How to Run Locally

**Prerequisites:** Node.js, PNPM, and Python 3.8+ must be installed.

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd fullstack-todo-app
    ```

2.  **Run the Backend:**
    ```bash
    # Open a terminal
    cd backend
    python -m venv venv
    source venv/bin/activate # On Windows: .\venv\Scripts\activate
    pip install "fastapi[all]"
    uvicorn main:app --reload
    ```
    *Your backend will be running at `http://localhost:8000`.*

3.  **Run the Frontend:**
    ```bash
    # Open a SECOND terminal
    cd frontend
    pnpm install
    pnpm dev
    ```
    *Your frontend will be running at `http://localhost:3000`.*

4.  Open `http://localhost:3000` in your browser to use the app!