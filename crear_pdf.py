from __future__ import annotations

import argparse
import textwrap
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from scripts.adrenalyn_checklist import DATA_FILE, GROUP_ORDER, card_lookup, load_document


PdfKind = Literal["repetidas", "faltantes", "stock"]
ROOT_DIR = Path(__file__).resolve().parent

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
PAGE_WIDTH, PAGE_HEIGHT = letter
LEFT_MARGIN = 42
RIGHT_MARGIN = 42
TOP_MARGIN = 54
BOTTOM_MARGIN = 42
COLUMN_GAP = 22
COLUMN_WIDTH = (PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN - COLUMN_GAP) / 2
LINE_HEIGHT = 10.5
GROUP_GAP = 5


@dataclass(frozen=True)
class PdfCard:
    group: str
    number: int
    name: str
    quantity: int = 1


def register_fonts() -> None:
    regular = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("DejaVuSans", regular))
        pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", bold))
        global FONT_REGULAR, FONT_BOLD
        FONT_REGULAR = "DejaVuSans"
        FONT_BOLD = "DejaVuSans-Bold"


def stock_quantities(document: dict[str, Any]) -> tuple[dict[int, int], list[str]]:
    lookup = card_lookup(document)
    quantities: dict[int, int] = defaultdict(int)
    warnings: list[str] = []
    stock = document.get("stock", {})

    if not isinstance(stock, dict):
        raise ValueError("El JSON debe contener la clave stock como objeto.")

    for stock_group, entries in stock.items():
        if not isinstance(entries, list):
            warnings.append(f"stock.{stock_group} no es una lista; se omite.")
            continue

        for entry in entries:
            if not isinstance(entry, dict):
                warnings.append(f"stock.{stock_group} contiene una entrada inválida; se omite.")
                continue

            number = entry.get("number")
            quantity = entry.get("quantity")
            if not isinstance(number, int):
                warnings.append(f"stock.{stock_group} contiene una tarjeta sin number entero.")
                continue
            if number not in lookup:
                warnings.append(f"stock.{stock_group} contiene la tarjeta inexistente {number}; se omite.")
                continue
            if not isinstance(quantity, int) or quantity < 1:
                warnings.append(f"stock.{stock_group} tarjeta {number} tiene quantity inválida; se omite.")
                continue

            expected_group, _ = lookup[number]
            if expected_group != stock_group:
                warnings.append(
                    f"stock.{stock_group} contiene {number}, que pertenece a {expected_group}; "
                    "se usa el grupo correcto en el PDF."
                )
            if number in quantities:
                warnings.append(f"stock contiene la tarjeta {number} más de una vez; se suman cantidades.")
            quantities[number] += quantity

    return dict(quantities), warnings


def build_pdf_cards(document: dict[str, Any], kind: PdfKind) -> tuple[dict[str, list[PdfCard]], list[str]]:
    lookup = card_lookup(document)
    quantities, warnings = stock_quantities(document)
    grouped: dict[str, list[PdfCard]] = {group: [] for group in GROUP_ORDER}

    for number in sorted(lookup):
        group, card = lookup[number]
        quantity = quantities.get(number, 0)

        if kind == "faltantes" and quantity == 0:
            grouped[group].append(PdfCard(group, number, card["name"]))
        elif kind == "repetidas" and quantity > 1:
            grouped[group].append(PdfCard(group, number, card["name"], quantity - 1))
        elif kind == "stock" and quantity > 0:
            grouped[group].append(PdfCard(group, number, card["name"], quantity))

    return grouped, warnings


def card_text(card: PdfCard, kind: PdfKind) -> str:
    suffix = ""
    if kind in {"repetidas", "stock"}:
        suffix = f" x{card.quantity}"
    return f"{card.number} - {card.name}{suffix}"


def wrap_card_text(text: str) -> list[str]:
    return textwrap.wrap(text, width=39, break_long_words=False, break_on_hyphens=False) or [text]


def draw_title(pdf: canvas.Canvas, title: str, subtitle: str) -> None:
    pdf.setFont(FONT_BOLD, 15)
    pdf.drawString(LEFT_MARGIN, PAGE_HEIGHT - 34, title)
    pdf.setFont(FONT_REGULAR, 8.5)
    pdf.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 30, subtitle)


def next_position(pdf: canvas.Canvas, column: int, page_number: int, title: str, subtitle: str) -> tuple[int, float, int]:
    if column == 0:
        return 1, PAGE_HEIGHT - TOP_MARGIN, page_number

    pdf.setFont(FONT_REGULAR, 8)
    pdf.drawCentredString(PAGE_WIDTH / 2, 22, f"Página {page_number}")
    pdf.showPage()
    page_number += 1
    draw_title(pdf, title, subtitle)
    return 0, PAGE_HEIGHT - TOP_MARGIN, page_number


def column_x(column: int) -> float:
    return LEFT_MARGIN + column * (COLUMN_WIDTH + COLUMN_GAP)


def render_pdf(grouped: dict[str, list[PdfCard]], kind: PdfKind, output: Path) -> None:
    register_fonts()

    titles = {
        "repetidas": "Tarjetas repetidas para intercambio",
        "faltantes": "Tarjetas faltantes",
        "stock": "Tarjetas en stock",
    }
    title = titles[kind]
    subtitle = "FIFA World Cup 2026 Adrenalyn XL - PANINI"

    pdf = canvas.Canvas(str(output), pagesize=letter)
    draw_title(pdf, title, subtitle)

    column = 0
    y = PAGE_HEIGHT - TOP_MARGIN
    page_number = 1
    total = sum(len(cards) for cards in grouped.values())

    for group in GROUP_ORDER:
        cards = grouped[group]
        if not cards:
            continue

        required_height = LINE_HEIGHT * 2 + GROUP_GAP
        if y - required_height < BOTTOM_MARGIN:
            column, y, page_number = next_position(pdf, column, page_number, title, subtitle)

        x = column_x(column)
        pdf.setFont(FONT_BOLD, 9.5)
        pdf.drawString(x, y, group)
        y -= LINE_HEIGHT + 1

        pdf.setFont(FONT_REGULAR, 8)
        for card in cards:
            lines = wrap_card_text(card_text(card, kind))
            required_height = LINE_HEIGHT * len(lines)
            if y - required_height < BOTTOM_MARGIN:
                column, y, page_number = next_position(pdf, column, page_number, title, subtitle)
                x = column_x(column)
                pdf.setFont(FONT_BOLD, 9.5)
                pdf.drawString(x, y, f"{group} (cont.)")
                y -= LINE_HEIGHT + 1
                pdf.setFont(FONT_REGULAR, 8)

            for line in lines:
                pdf.drawString(x, y, line)
                y -= LINE_HEIGHT

        y -= GROUP_GAP

    pdf.setFont(FONT_REGULAR, 8)
    pdf.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, 22, f"Total: {total}")
    pdf.drawCentredString(PAGE_WIDTH / 2, 22, f"Página {page_number}")
    pdf.save()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crear PDF desde data/figuritas.json usando checklist y stock."
    )
    parser.add_argument(
        "tipo",
        nargs="?",
        choices=["repetidas", "faltantes", "stock"],
        default="repetidas",
        help='Elija "repetidas", "faltantes" o "stock" (por defecto: repetidas).',
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Ruta de salida del PDF. Por defecto usa listado-{tipo}.pdf.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    kind: PdfKind = args.tipo
    output = args.output or ROOT_DIR / f"listado-{kind}.pdf"
    document = load_document(DATA_FILE)
    grouped, warnings = build_pdf_cards(document, kind)
    render_pdf(grouped, kind, output)

    for warning in warnings:
        print(f"Advertencia: {warning}")

    total = sum(len(cards) for cards in grouped.values())
    print(f"PDF creado correctamente: {output} ({total} tarjetas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
