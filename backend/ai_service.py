import json
import os
import requests

AI_MODE = os.getenv("AI_MODE", "ollama")

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


def analyze_ticket(title: str, description: str):
    if AI_MODE == "mock":
        return mock_analysis(title, description)

    return ollama_analysis(title, description)


def ollama_analysis(title: str, description: str):
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


def mock_analysis(title: str, description: str):
    return {
        "category": "General Support",
        "priority": "Medium",
        "summary": description[:100],
        "suggested_action": "Review the issue and assign it to the appropriate support team."
    }