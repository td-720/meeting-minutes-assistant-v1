from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import dotenv_values
from google import genai

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_minutes(transcript_text: str, speaker_notes: str, reference_text_or_prompt: str) -> dict[str, Any]:
    local_values = dotenv_values(Path(__file__).resolve().parents[1] / ".env")
    file_key = str(local_values.get("GEMINI_API_KEY") or "").strip()
    api_key = file_key if file_key and not file_key.lower().startswith("replace-with-") else os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add your key to the local .env file.")

    client = genai.Client(api_key=api_key)
    schema = {
        "type": "OBJECT",
        "properties": {
            "minutes_text": {"type": "STRING"},
            "unclear_attributions": {"type": "ARRAY", "items": {"type": "STRING"}},
        },
        "required": ["minutes_text", "unclear_attributions"],
        "propertyOrdering": ["minutes_text", "unclear_attributions"],
    }
    prompt = f"""Create complete draft minutes for an in-person meeting.

Requirements:
- Follow the supplied reference or requested structure, including headings and their order.
- Use only facts supported by the transcript and secretary notes. Do not invent events, decisions, dates, names, or commitments.
- Use speaker notes to attribute statements. Never guess an unclear speaker. Leave uncertain attribution blank in the minutes and list what needs clarification in unclear_attributions.
- Be concise but complete, and clearly distinguish discussion, decisions, and actions when supported.

SECRETARY'S FORMAT GUIDANCE OR REFERENCE:
{reference_text_or_prompt}

SECRETARY'S SPEAKER NOTES:
{speaker_notes}

MEETING TRANSCRIPT:
{transcript_text}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={"response_mime_type": "application/json", "response_json_schema": schema, "temperature": 0.2},
    )
    raw = getattr(response, "text", None)
    if not raw:
        raise RuntimeError("The AI returned an empty response. Your draft inputs have been preserved; try again.")
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("The AI response was not valid structured data. Your draft inputs have been preserved; try again.") from exc
    minutes = result.get("minutes_text")
    flags = result.get("unclear_attributions", [])
    if not isinstance(minutes, str) or not minutes.strip() or not isinstance(flags, list):
        raise RuntimeError("The AI response did not match the expected minutes format. Your draft inputs have been preserved; try again.")
    return {"minutes_text": minutes.strip(), "unclear_attributions": [str(item) for item in flags]}
