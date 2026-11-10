# Rebel-AI
This AI i created for my own use. It is working absolutly osm.

Structure of my Project:

REBEL-AI/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── memory/
│       ├── __init__.py
│       └── facts.py
│
├── frontend/
│   └── index.html
│
├── data/
│   └── .gitkeep
│
├── requirements.txt
├── .gitignore
├── README.md
└── test_memory.py

Installation commands for users:

Windows – Command Prompt:

git clone YOUR_GITHUB_REPOSITORY_URL
cd REBEL-AI

python -m venv .venv
.venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

ollama pull qwen2.5:3b

uvicorn backend.main:app --host 127.0.0.1 --port 8000

Mac – Terminal:

git clone YOUR_GITHUB_REPOSITORY_URL
cd REBEL-AI

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

ollama pull qwen2.5:3b

uvicorn backend.main:app --host 127.0.0.1 --port 8000

Then open http://127.0.0.1:8000/app/








