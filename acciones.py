DESPLAZAMIENTOS = {
    "arriba": (-1, 0),
    "abajo": (1, 0),
    "izquierda": (0, -1),
    "derecha": (0, 1),
}

def calcular_destino(posicion, direccion):
    fila, columna = posicion
    cambio_fila, cambio_columna = DESPLAZAMIENTOS[direccion]

    return fila + cambio_fila, columna + cambio_columna

def esta_dentro_del_mapa(mapa, posicion):
    fila, columna = posicion

    return (
        0 <= fila < len(mapa)
        and 0 <= columna < len(mapa[fila])
    )

def es_transitable(mapa, posicion):
    if not esta_dentro_del_mapa(mapa, posicion):
        return False

    fila, columna = posicion
    casilla = mapa[fila][columna]

    return casilla not in ("#", "D")

def comprobar_partida_activa(estado):
    if estado["terminado"]:
        return {"exito": False, "mensaje": "La partida ya terminó."}
    estado["pasos"] += 1
    if estado["pasos"] >= estado["max_pasos"]:
        estado["terminado"] = True
        estado["motivo_fin"] = "limite_pasos"

    return None

def mover(estado, direccion):

    error = comprobar_partida_activa(estado)
    if error is not None:
        return error

    if direccion not in DESPLAZAMIENTOS:
        return {"exito": False, "mensaje": "Dirección desconocida."}

    destino = calcular_destino(estado["posicion_jugador"], direccion)

    if not esta_dentro_del_mapa(estado["mapa"], destino):
        return {"exito": False, "mensaje": "Movimiento inválido: fuera del mapa."}

    if not es_transitable(estado["mapa"], destino):
        fila, columna = destino
        if estado["mapa"][fila][columna] == "#":
            mensaje = "Movimiento inválido: hay una pared."
        else:
            mensaje = "Movimiento inválido: hay una puerta cerrada."

        return {"exito": False, "mensaje": mensaje}

    estado["posicion_jugador"] = destino
    if ha_ganado(estado):
        estado["terminado"] = True
        estado["motivo_fin"] = "victoria"
        return {"exito": True, "mensaje": "¡Misión completada!"}
    
    return {"exito": True, "mensaje": "Movimiento valido."}

def recoger(estado):

    error = comprobar_partida_activa(estado)
    if error is not None:
        return error

    fila, columna = estado["posicion_jugador"]

    if estado["mapa"][fila][columna] != "K":
        return {"exito": False, "mensaje": "Aquí no hay una llave."}

    estado["tiene_llave"] = True

    contenido = estado["mapa"][fila]
    estado["mapa"][fila] = contenido[:columna] + "." + contenido[columna + 1:]

    return {"exito": True, "mensaje": "Has recogido la llave."}

def abrir(estado, direccion):

    error = comprobar_partida_activa(estado)
    if error is not None:
        return error

    if direccion not in DESPLAZAMIENTOS:
        return {"exito": False, "mensaje": "Dirección desconocida."}

    destino = calcular_destino(estado["posicion_jugador"], direccion)

    if not esta_dentro_del_mapa(estado["mapa"], destino):
        return {"exito": False, "mensaje": "Fuera del mapa."}

    fila, columna = destino

    if estado["mapa"][fila][columna] != "D":
        return {"exito": False, "mensaje": "No hay una puerta ahí."}

    if not estado["tiene_llave"]:
        return {"exito": False, "mensaje": "Necesitas la llave."}

    contenido = estado["mapa"][fila]
    estado["mapa"][fila] = contenido[:columna] + "." + contenido[columna + 1:]

    return {"exito": True, "mensaje": "Puerta abierta."}

def ha_ganado(estado):
    fila, columna = estado["posicion_jugador"]
    return estado["mapa"][fila][columna] == "S"

def observar(estado):
    return {
        "mapa": estado["mapa"].copy(),
        "posicion_jugador": estado["posicion_jugador"],
        "tiene_llave": estado["tiene_llave"],
        "pasos": estado["pasos"],
        "max_pasos": estado["max_pasos"],
        "terminado": estado["terminado"],
        "motivo_fin": estado["motivo_fin"],
        "semilla": estado["semilla"],
    }