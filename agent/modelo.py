from langchain_groq import ChatGroq

from agent.config import cargar_configuracion
from agent.tools import TOOLS

def crear_modelo():
    clave, nombre_modelo = cargar_configuracion()

    return ChatGroq(
        model=nombre_modelo,
        api_key=clave,
        temperature=0,
        reasoning_effort="low",
        max_tokens=2048,
        timeout=30,
        max_retries=0,
    )

def create_agent_model():
    modelo = crear_modelo()
    # El modelo considera las herramientas sin ejecutarlas.
    return modelo.bind_tools(TOOLS) 