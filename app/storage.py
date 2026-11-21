"""Load and validate employee skill sequences."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA = ROOT / "data" / "employee_sequences.json"


def load_sequences(path: str | Path | None = None) -> list[dict]:
    source = Path(path) if path else DEFAULT_DATA
    records = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not records:
        raise ValueError("Dataset must be a non-empty JSON list.")
    cleaned = []
    for i, row in enumerate(records, 1):
        if not isinstance(row, dict) or not isinstance(row.get("skills"), list):
            raise ValueError(f"Record {i} must contain a skills list.")
        skills = [str(s).strip() for s in row["skills"] if str(s).strip()]
        if len(skills) < 2:
            raise ValueError(f"Record {i} needs at least two chronological skills.")
        cleaned.append({"employee_id": str(row.get("employee_id", f"employee-{i}")),
                        "role": str(row.get("role", "Unspecified")),
                        "skills": skills})
    return cleaned
