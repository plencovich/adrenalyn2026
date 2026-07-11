from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.adrenalyn_checklist import (
    ALLOWED_POSITIONS,
    COLLECTION,
    DATA_FILE,
    GROUP_ORDER,
    RANGE_BY_GROUP,
    cards_for_group,
    load_document,
    resolve_card,
    validate_document,
    with_derived_inventory,
)


class AdrenalynChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = load_document(DATA_FILE)
        cls.cards = [
            card
            for group in GROUP_ORDER
            for card in cls.document["checklist"][group]
        ]

    def test_total_cards(self) -> None:
        self.assertEqual(len(self.cards), COLLECTION["total_cards"])

    def test_first_card_is_one(self) -> None:
        self.assertEqual(self.cards[0]["number"], 1)

    def test_last_card_is_630(self) -> None:
        self.assertEqual(self.cards[-1]["number"], 630)

    def test_no_missing_numbers(self) -> None:
        self.assertEqual(
            [card["number"] for card in self.cards],
            list(range(1, COLLECTION["total_cards"] + 1)),
        )

    def test_no_duplicate_numbers(self) -> None:
        numbers = [card["number"] for card in self.cards]
        self.assertEqual(len(numbers), len(set(numbers)))

    def test_ranges_by_country_and_category(self) -> None:
        for group, (start, end) in RANGE_BY_GROUP.items():
            numbers = [card["number"] for card in self.document["checklist"][group]]
            self.assertEqual(numbers, list(range(start, end + 1)), group)

    def test_allowed_positions(self) -> None:
        for card in self.cards:
            position = card["position"]
            self.assertTrue(position is None or position in ALLOWED_POSITIONS)

    def test_utf8_serialization(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "figuritas.json"
            with path.open("w", encoding="utf-8") as file:
                json.dump(self.document, file, ensure_ascii=False, indent=2)
            serialized = path.read_text(encoding="utf-8")
            self.assertIn("JULIÁN ÁLVAREZ", serialized)

    def test_resolve_card_by_number(self) -> None:
        card = resolve_card(self.document, 22)
        self.assertEqual(card["name"], "JULIÁN ÁLVAREZ")
        self.assertEqual(card["position"], "fan_favourite")

    def test_resolve_cards_for_group(self) -> None:
        cards = cards_for_group(self.document, "ARG")
        self.assertEqual(len(cards), 12)
        self.assertEqual(cards[0]["number"], 22)

    def test_stock_derives_repetidas_and_faltantes(self) -> None:
        document = copy.deepcopy(self.document)
        document["stock"]["ARG"] = [{"number": 22, "quantity": 3}]
        document = with_derived_inventory(document)

        repeated_numbers = [card["number"] for card in document["repetidas"]["ARG"]]
        missing_numbers = [card["number"] for card in document["faltantes"]["ARG"]]
        self.assertEqual(repeated_numbers, [22, 22])
        self.assertNotIn(22, missing_numbers)
        self.assertFalse(validate_document(document))

    def test_empty_stock_marks_all_cards_as_faltantes(self) -> None:
        document = copy.deepcopy(self.document)
        document["stock"] = {group: [] for group in GROUP_ORDER}
        document = with_derived_inventory(document)
        missing_total = sum(len(cards) for cards in document["faltantes"].values())
        repeated_total = sum(len(cards) for cards in document["repetidas"].values())
        self.assertEqual(missing_total, COLLECTION["total_cards"])
        self.assertEqual(repeated_total, 0)

    def test_reject_nonexistent_card(self) -> None:
        with self.assertRaises(KeyError):
            resolve_card(self.document, 999)

    def test_reject_empty_names(self) -> None:
        document = copy.deepcopy(self.document)
        document["checklist"]["ARG"][0]["name"] = ""
        self.assertTrue(any("empty" in error for error in validate_document(document)))

    def test_reject_unknown_positions(self) -> None:
        document = copy.deepcopy(self.document)
        document["checklist"]["ARG"][0]["position"] = "striker"
        self.assertTrue(any("invalid position" in error for error in validate_document(document)))

    def test_reject_invalid_stock_quantity(self) -> None:
        document = copy.deepcopy(self.document)
        document["stock"]["ARG"] = [{"number": 22, "quantity": 0}]
        document = with_derived_inventory(document)
        self.assertTrue(any("quantity >= 1" in error for error in validate_document(document)))

    def test_reject_manual_derived_inventory_drift(self) -> None:
        document = copy.deepcopy(self.document)
        document["faltantes"]["ARG"] = []
        self.assertTrue(any("faltantes must be derived" in error for error in validate_document(document)))


if __name__ == "__main__":
    unittest.main()
