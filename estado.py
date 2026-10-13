from laberinto import generar_con_reintentos
from validacion import validar_mision
import random

def crear_estado_inicial(semilla = None):
    if semilla is None:
        semilla = random.randrange(1000000)
    mapa, semilla = generar_con_reintentos(semilla)
    estado ={
        "mapa": mapa,
        "posicion_jugador": (1, 1),
        "tiene_llave": False,
        "terminado": False,
        "pasos": 0,
        "max_pasos": 300,
        "semilla": semilla,
        "motivo_fin": None
    }
    
    if not validar_mision(estado):
        raise ValueError(
            f"El mapa con semilla {semilla} no cumple las reglas de la misión."
        )
    
    return estado   
