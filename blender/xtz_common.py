from __future__ import annotations

import json
import os
from pathlib import Path


def repo_root() -> Path:
    """Resolve repository root for Blender or command-line execution."""
    env = os.environ.get("XTZ_REPO_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    here = Path(__file__).resolve()
    return here.parents[1]


def load_world_json(filename: str) -> dict:
    path = repo_root() / "data" / "world" / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing canonical world data: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_positive(value, label: str) -> float:
    value = float(value)
    if value <= 0:
        raise ValueError(f"{label} must be positive, got {value}")
    return value
