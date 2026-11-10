
import json
import httpx

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:3b"


async def extract_facts(message: str):
    prompt = f"""
You are REBEL AI's personal memory extraction engine.

Read the user's entire message carefully.

Extract EVERY explicitly stated, useful personal fact.
Do not stop after finding one fact.

Extract facts about:
- Name and personal identity
- Education and qualifications
- Career and employment
- Technical and non-technical skills
- Learning activities
- Career goals
- Long-term preferences
- Personal projects

Rules:
1. Extract multiple facts from one message.
2. Each fact must be independent.
3. Never invent or assume information.
4. Do not extract questions or hypothetical statements.
5. Preserve the meaning of the user's words.
6. Return an empty facts list if nothing useful is stated.
7. Return valid JSON only.

Example:
User: My name is Roshan. I studied Computer Science.
Output:
{{
  "facts": [
    {{
      "category": "personal",
      "key": "name",
      "value": "Roshan"
    }},
    {{
      "category": "education",
      "key": "degree_field",
      "value": "Computer Science"
    }}
  ]
}}

User message:
{message}
"""


    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0
                    }
                }
            )

            response.raise_for_status()
            result = response.json()

        extracted = json.loads(
            result["message"]["content"]
        )

        facts = extracted.get("facts", [])

        if not isinstance(facts, list):
            return []

        allowed_categories = {
            "personal", "career", "education",
            "skills", "preferences", "goals", "projects"
        }

        valid_facts = []

        for fact in facts:
            if not isinstance(fact, dict):
                continue

            category = fact.get("category")
            key = fact.get("key")
            value = fact.get("value")

            if (
                category in allowed_categories
                and isinstance(key, str)
                and isinstance(value, str)
                and key.strip()
                and value.strip()
            ):
                valid_facts.append({
                    "category": category,
                    "key": key.strip(),
                    "value": value.strip()
                })

        return valid_facts

    except (httpx.HTTPError, json.JSONDecodeError, KeyError):
        return []
