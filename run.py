import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import your chatbot logic (src/agent_interface.py etc.)
from src.agent_interface import ask_question

app = FastAPI()

# -----------------------------
# Serve React frontend
# -----------------------------

# Path to built React files
frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")

# Mount static assets (JS, CSS, etc.)
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

# Serve index.html on root
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_dist, "index.html"))


# -----------------------------
# API Endpoint for chatbot
# -----------------------------

class Query(BaseModel):
    question: str

@app.post("/query")
async def query_agent(request: Query):
    try:
        answer = ask_question(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
