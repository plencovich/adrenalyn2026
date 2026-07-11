from __future__ import annotations

from adrenalyn_checklist import DATA_FILE, load_document, validate_document


def main() -> int:
    document = load_document(DATA_FILE)
    errors = validate_document(document)
    if errors:
        print("Checklist validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    total_cards = sum(len(cards) for cards in document["checklist"].values())
    print(f"Checklist validation OK: {total_cards} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
