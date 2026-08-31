import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


def analyze_ticket(title: str, description: str):

    prompt = f"""
You are an AI support ticket assistant.

Analyze this support ticket.

Title: {title}
Description: {description}

Return ONLY valid JSON with this exact structure:

{{
  "category": "string",
  "priority": "Low, Medium, or High",
  "summary": "short summary",
  "suggested_action": "short recommended action"
}}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return json.loads(data["response"])