# Rebel-AI
This AI i created for my own use. It is working absolutly osm.

Structure of my Project:
<img width="346" height="401" alt="Screenshot 2026-11-10 at 11 24 35 AM" src="https://github.com/user-attachments/assets/5277e862-01d8-44f5-9712-2f884cdac100" />

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








