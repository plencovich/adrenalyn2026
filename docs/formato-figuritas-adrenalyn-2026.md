# Formato de figuritas Adrenalyn XL 2026

`data/figuritas.json` contiene la colección `FIFA World Cup 2026 Adrenalyn XL` de Panini con
numeración global del 1 al 630.

## Estructura

```json
{
  "collection": {
    "name": "FIFA World Cup 2026 Adrenalyn XL",
    "publisher": "Panini",
    "total_cards": 630,
    "numbering": "global"
  },
  "checklist": {
    "ARG": [
      {
        "number": 22,
        "name": "JULIÁN ÁLVAREZ",
        "position": "fan_favourite"
      }
    ]
  },
  "stock": {
    "ARG": [
      {
        "number": 22,
        "quantity": 2
      }
    ]
  },
  "repetidas": {
    "ARG": [
      {
        "number": 22,
        "name": "JULIÁN ÁLVAREZ",
        "position": "fan_favourite"
      }
    ]
  },
  "faltantes": {
    "ARG": []
  }
}
```

`checklist` es el catálogo maestro. `stock` es el único inventario editable. Cada entrada de
`stock` necesita `number` y `quantity`; nombre y posición se resuelven desde el catálogo.

`repetidas` y `faltantes` son vistas derivadas de `stock` para mantener compatibilidad con el JSON.
La web y el generador de PDFs también las recalculan al leer. No se editan manualmente.

## Posiciones

Valores permitidos:

- `goalkeeper`
- `defender`
- `midfielder`
- `forward`
- `fan_favourite`
- `icon`
- `null`

`null` se usa para tarjetas sin posición o tipo confiable, por ejemplo `TEAM CREST`, los cruces
iniciales de `CONTENDERS` y algunas tarjetas de `VARIOS`.

## Inventario

`stock` contiene las tarjetas que tenés físicamente:

```json
{
  "number": 22,
  "quantity": 2
}
```

Reglas:

- Si una tarjeta no aparece en `stock`, queda en `faltantes`.
- Si `quantity` es `1`, la tarjeta está en stock pero no en `repetidas`.
- Si `quantity` es mayor a `1`, `repetidas` contiene `quantity - 1` copias de esa tarjeta.

`repetidas` conserva arrays para permitir múltiples copias físicas de una misma tarjeta. No se
eliminan duplicados automáticamente. `faltantes` se genera con una sola entrada por tarjeta no
presente en `stock`.

## Generación y Validación

La fuente estructurada está en `scripts/adrenalyn_checklist.py`. El PDF oficial incluido en el
root es image-based, por lo que la extracción OCR no forma parte del runtime de la aplicación.

Comandos:

```bash
python3 scripts/build_adrenalyn_checklist.py
python3 scripts/validate_adrenalyn_checklist.py
python3 -m unittest discover -s tests
```

La validación comprueba total, huecos, duplicados, rangos, posiciones permitidas, coherencia entre
catálogo y `stock`, cantidades válidas, y que `repetidas`/`faltantes` coincidan con lo derivado.

## Normalización

Las categorías especiales usan keys propias y no se tratan como países:

`GOLDEN_BALLERS`, `CONTENDERS`, `TOP_KEEPERS`, `DEFENSIVE_ROCKS`, `MIDFIELD_MAESTROS`,
`GOAL_MACHINES`, `MASTER_ROOKIES`, `VARIOS`.

Rangos especiales actualizados:

- `CONTENDERS`: 514-549
- `MASTER_ROOKIES`: 608-623
- `VARIOS`: 624-630
