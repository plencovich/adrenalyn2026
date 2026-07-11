# Canje de figuritas Mundial 2026

Sitio estático responsive para seleccionar figuritas repetidas y faltantes, armar una propuesta de
canje y enviarla por WhatsApp. El mismo archivo JSON alimenta la web y la generación de PDFs.

## Fuente de datos

`data/figuritas.json` es la única fuente de verdad:

```json
{
  "collection": {
    "name": "FIFA World Cup 2026 Adrenalyn XL",
    "publisher": "Panini",
    "total_cards": 620,
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

La colección usa numeración global de tarjeta. `checklist` contiene el catálogo maestro de 620
tarjetas y `stock` es el inventario editable: agregá `number` y `quantity`, y ejecutá el generador.
`repetidas` y `faltantes` son vistas derivadas de `stock`: no se editan a mano. La web y el
generador de PDFs también recalculan esas vistas al leer el JSON.

La web agrega automáticamente un parámetro de versión al solicitar el JSON y desactiva la caché
del navegador para que los cambios publicados se carguen sin reutilizar una copia anterior.

La estructura completa está documentada en
[`docs/formato-figuritas-adrenalyn-2026.md`](docs/formato-figuritas-adrenalyn-2026.md).

## Probar localmente

La web usa `fetch`, por lo que no conviene abrir `index.html` directamente con `file://`. Desde la
raíz del proyecto ejecutá:

```bash
python3 -m http.server 8000
```

Luego abrí `http://localhost:8000`.

## Configurar WhatsApp

En `assets/js/app.js`, reemplazá:

```js
const WHATSAPP_PHONE = "549XXXXXXXXXX"
```

por el número real en formato internacional, sin `+`, espacios ni guiones. Para Argentina, el
formato habitual para WhatsApp incluye `54` y `9` antes del código de área.

## Generar los PDFs

Instalá ReportLab si todavía no está disponible:

```bash
python3 -m pip install reportlab
```

Generá cada listado con:

```bash
python3 crear_pdf.py repetidas
python3 crear_pdf.py faltantes
```

Sin argumento se genera `listado-repetidas.pdf`, igual que en el flujo original. `crear_pdf.py`
sigue usando el mismo diseño, argumentos y nombres de salida; lee `stock` desde
`data/figuritas.json` y calcula el listado correspondiente.

## Generar y validar el checklist

El checklist se regenera desde la fuente estructurada transcrita en
`scripts/adrenalyn_checklist.py`. El generador preserva el `stock` existente y recalcula
`repetidas`/`faltantes`:

```bash
python3 scripts/build_adrenalyn_checklist.py
python3 scripts/validate_adrenalyn_checklist.py
python3 -m unittest discover -s tests
```

## Publicar en GitHub Pages

1. Subí el proyecto a un repositorio de GitHub.
2. En el repositorio, abrí **Settings > Pages**.
3. En **Build and deployment**, elegí **Deploy from a branch**.
4. Seleccioná la rama principal (`main`) y la carpeta raíz (`/ root`).
5. Guardá y esperá a que GitHub publique la URL.

No se requiere backend, base de datos ni proceso de compilación.

## Documentación técnica

- [Formato FIFA World Cup 2026 Adrenalyn XL](docs/formato-figuritas-adrenalyn-2026.md)
- [Desarrollo HTML para canje de figuritas](docs/prompts/desarrollo-html-canje-figuritas.md)
