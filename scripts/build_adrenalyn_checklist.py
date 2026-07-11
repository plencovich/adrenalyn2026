from __future__ import annotations

import json
from pathlib import Path

from adrenalyn_checklist import (
    DATA_FILE,
    build_document,
    load_document,
    validate_document,
    with_derived_inventory,
)


def write_json(path: Path = DATA_FILE) -> None:
    document = build_document()
    if path.exists():
        current = load_document(path)
        if isinstance(current.get("stock"), dict):
            document["stock"] = current["stock"]
            document = with_derived_inventory(document)

    errors = validate_document(document)
    if errors:
        joined = "\n".join(f"- {error}" for error in errors)
        raise SystemExit(f"Checklist validation failed before writing JSON:\n{joined}")

    with path.open("w", encoding="utf-8") as file:
        json.dump(document, file, ensure_ascii=False, indent=2)
        file.write("\n")


if __name__ == "__main__":
    write_json()
    print(f"Checklist written to {DATA_FILE}")
