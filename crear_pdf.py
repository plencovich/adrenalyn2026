from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import argparse
from typing import Any, TypedDict

from scripts.adrenalyn_checklist import DATA_FILE, load_document, with_derived_inventory


# El JSON es la única fuente de verdad para el PDF y la web. El stock editable se
# expande a repetidas/faltantes al leer para evitar listados derivados obsoletos.
figuritas = with_derived_inventory(load_document(DATA_FILE))
dataRepetidas = figuritas["repetidas"]
dataFaltantes = figuritas["faltantes"]


class CardEntry(TypedDict):
    number: int
    name: str
    position: str | None


def card_number(card: dict[str, Any]) -> int:
    number = card.get("number")
    if not isinstance(number, int):
        raise ValueError(f"Entrada de figurita inválida, falta number entero: {card!r}")
    return number


def preparar_datos_para_pdf(data: dict[str, list[CardEntry]]) -> dict[str, list[int]]:
    datos_pdf: dict[str, list[int]] = {}

    for group_key, cards in data.items():
        if not isinstance(cards, list):
            raise ValueError(f"La clave {group_key} debe contener una lista de tarjetas.")
        datos_pdf[group_key] = [card_number(card) for card in sorted(cards, key=card_number)]

    return datos_pdf

# Selección de dataset según argumento CLI
parser = argparse.ArgumentParser(description="Crear PDF listado de países")
parser.add_argument(
    "tipo",
    nargs="?",
    choices=["repetidas", "faltantes"],
    default="repetidas",
    help='Elija "repetidas" o "faltantes" (por defecto: repetidas)',
)
args = parser.parse_args()

if args.tipo == "repetidas":
    data = preparar_datos_para_pdf(dataRepetidas)
else:
    data = preparar_datos_para_pdf(dataFaltantes)

# Nombre del archivo PDF según el tipo
pdf_file = f"listado-{args.tipo}.pdf"

# Título dinámico según el tipo
title_text = "Repetidas" if args.tipo == "repetidas" else "Faltantes"

# Crear PDF
c = canvas.Canvas(pdf_file, pagesize=letter)
width, height = letter

# Título
c.setFont("Helvetica-Bold", 16)
c.drawString(180, height - 40, title_text)

# Configuración de columnas
left_x = 50
right_x = 320

start_y = height - 80
line_height = 16

# Ordenar los países alfabéticamente
items = sorted(data.items())
half = (len(items) + 1) // 2

left_column = items[:half]
right_column = items[half:]

# Fuente
c.setFont("Helvetica", 10)

# Columna izquierda
y_left = start_y
for country, numbers in left_column:
    line = f"{country}: {', '.join(map(str, numbers))}"
    c.drawString(left_x, y_left, line)
    y_left -= line_height

# Columna derecha
y_right = start_y
for country, numbers in right_column:
    line = f"{country}: {', '.join(map(str, numbers))}"
    c.drawString(right_x, y_right, line)
    y_right -= line_height

# Guardar PDF
c.save()

print(f"PDF creado correctamente: {pdf_file}")
