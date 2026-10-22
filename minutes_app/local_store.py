from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

APP_DIR = Path.home() / ".meeting-minutes-assistant"
TEMPLATES_DIR = APP_DIR / "templates"
TEMPLATES_INDEX = APP_DIR / "templates.json"
DRAFT_PATH = APP_DIR / "current_draft.json"


def ensure_app_dirs() -> None:
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    ensure_app_dirs()
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def load_draft() -> dict[str, Any]:
    ensure_app_dirs()
    if not DRAFT_PATH.exists():
        return {}
    try:
        data = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_draft(data: dict[str, Any]) -> None:
    _write_json(DRAFT_PATH, data)


def clear_draft() -> None:
    DRAFT_PATH.unlink(missing_ok=True)


def list_templates() -> list[dict[str, str]]:
    ensure_app_dirs()
    try:
        entries = json.loads(TEMPLATES_INDEX.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict) and entry.get("id") and entry.get("name")]


def get_template(template_id: str) -> dict[str, str] | None:
    return next((item for item in list_templates() if item.get("id") == template_id), None)


def add_template(name: str, extension: str, content: bytes, text: str) -> dict[str, str]:
    import uuid

    ensure_app_dirs()
    allowed = {".docx", ".pdf", ".txt"}
    suffix = extension.lower()
    if suffix not in allowed:
        raise ValueError("Only DOCX, text-readable PDF, and TXT templates are supported.")
    template_id = uuid.uuid4().hex
    target = TEMPLATES_DIR / f"{template_id}{suffix}"
    target.write_bytes(content)
    entry = {"id": template_id, "name": name.strip() or f"Template {len(list_templates()) + 1}", "extension": suffix, "path": str(target), "text": text}
    entries = list_templates()
    entries.append(entry)
    temporary = TEMPLATES_INDEX.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(TEMPLATES_INDEX)
    return entry
