import json
from pathlib import Path
from typing import Any, Dict

# Default manifest location is project root
DEFAULT_PATH = Path(__file__).resolve().parents[1] / 'capability_manifest.json'


def load_manifest(path: str | Path | None = DEFAULT_PATH) -> Dict[str, Any]:
    """Load and return the capability manifest."""
    if path is None:
        path = DEFAULT_PATH
    path = Path(path)
    with path.open() as f:
        return json.load(f)
