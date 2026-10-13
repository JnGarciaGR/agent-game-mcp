import os
from pathlib import Path

from dotenv import load_dotenv


def cargar_configuracion():
    ruta_env = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(ruta_env)

    clave = os.getenv("GROQ_API_KEY")
    modelo = os.getenv("GROQ_MODEL")

    if not clave or not modelo:
        raise ValueError("Falta GROQ_API_KEY o GROQ_MODEL en la configuración.")

    return clave, modelo