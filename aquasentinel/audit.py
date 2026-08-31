from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path


def record(event: str, data: dict, path: str = "audit/aquasentinel.jsonl") -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    row = {"timestamp": datetime.now(timezone.utc).isoformat(), "event": event, "data": data}
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
