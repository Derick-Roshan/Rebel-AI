
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import sqlite3
import httpx

app = FastAPI(title="REBEL AI")

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "rebel_memory.db"

# Local AI configuration
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:3b"


# Database connection
def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# Create database and messages table
def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


initialize_database()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "name": "REBEL AI",
        "status": "Online",
        "engine": "Local Ollama",
        "memory": "SQLite"
    }


# Retrieve previous conversations
@app.get("/history")
def get_history():
    with get_db() as connection:
        rows = connection.execute("""
            SELECT id, role, content, created_at
            FROM messages
            ORDER BY id DESC
            LIMIT 30
        """).fetchall()

    return {
        "messages": [dict(row) for row in reversed(rows)]
    }


# Send message to local AI and save conversation
@app.post("/chat")
async def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    # Load recent conversation context
    with get_db() as connection:
        rows = connection.execute("""
            SELECT role, content
            FROM messages
            ORDER BY id DESC
            LIMIT 20
        """).fetchall()

    history = [
        {"role": row["role"], "content": row["content"]}
        for row in reversed(rows)
    ]

    messages = [
        {
            "role": "system",
            "content": (
                "You are REBEL AI, a private personal assistant. "
                "You run locally and should be helpful, accurate "
                "and direct. Use previous conversation context "
                "when relevant. Never claim to remember something "
                "that is not in the supplied context."
            )
        }
    ]

    messages.extend(history)
    messages.append({
        "role": "user",
        "content": message
    })

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": False
                }
            )

            response.raise_for_status()
            result = response.json()

        reply = result["message"]["content"]

        # Save both messages locally
        with get_db() as connection:
            connection.executemany("""
                INSERT INTO messages (role, content)
                VALUES (?, ?)
            """, [
                ("user", message),
                ("assistant", reply)
            ])

        return {
            "assistant": "REBEL AI",
            "reply": reply
        }

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=503,
            detail=f"Local AI engine unavailable: {error}"
        )


# Serve the custom frontend
app.mount(
    "/app",
    StaticFiles(directory=str(BASE_DIR / "frontend"), html=True),
    name="frontend"
)
