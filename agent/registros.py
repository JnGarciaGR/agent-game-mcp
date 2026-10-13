import json
from pathlib import Path
from uuid import uuid4


def guardar_resultado(resumen):
    carpeta = Path(__file__).resolve().parent.parent / "resultados"
    carpeta.mkdir(exist_ok=True)

    ruta = carpeta / f"partida_{uuid4().hex}.json"
    contenido = json.dumps(resumen, ensure_ascii=False, indent=2)
    ruta.write_text(contenido, encoding="utf-8")

    return ruta