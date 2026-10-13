from acciones import DESPLAZAMIENTOS, calcular_destino, es_transitable
from collections import deque

def casillas_alcanzables(mapa, inicio):
    pendientes = [inicio]
    visitadas = {inicio}

    while pendientes:
        posicion = pendientes.pop()

        for direccion in DESPLAZAMIENTOS:
            destino = calcular_destino(posicion, direccion)

            if es_transitable(mapa, destino) and destino not in visitadas:
                visitadas.add(destino)
                pendientes.append(destino)

    return visitadas

def llave_es_accesible(estado):
    mapa = estado["mapa"]
    inicio = estado["posicion_jugador"]
    alcanzables = casillas_alcanzables(mapa, inicio)

    for fila, columna in alcanzables:
        if mapa[fila][columna] == "K":
            return True

    return False

def salida_accesible_al_abrir(estado):
    mapa_abierto = [
        fila.replace("D", ".")
        for fila in estado["mapa"]
    ]

    alcanzables = casillas_alcanzables(
        mapa_abierto, estado["posicion_jugador"]
    )

    for fila, columna in alcanzables:
        if mapa_abierto[fila][columna] == "S":
            return True

    return False

def validar_mision(estado):
    if not llave_es_accesible(estado):
        return False

    if not salida_accesible_al_abrir(estado):
        return False

    alcanzables = casillas_alcanzables(
        estado["mapa"], estado["posicion_jugador"]
    )

    for fila, columna in alcanzables:
        if estado["mapa"][fila][columna] == "S":
            return False

    return True

def calcular_distancias(mapa, inicio):
    distancias = {inicio: 0}
    pendientes = deque([inicio])

    while pendientes:
        posicion = pendientes.popleft()

        for direccion in DESPLAZAMIENTOS:
            destino = calcular_destino(posicion, direccion)

            if es_transitable(mapa, destino) and destino not in distancias:
                distancias[destino] = distancias[posicion] + 1
                pendientes.append(destino)

    return distancias

def reconstruir_camino(mapa, inicio, destino):
    distancias = calcular_distancias(mapa, inicio)

    if destino not in distancias:
        return []

    camino = [destino]

    while camino[-1] != inicio:
        actual = camino[-1]

        for direccion in DESPLAZAMIENTOS:
            vecino = calcular_destino(actual, direccion)

            if distancias.get(vecino) == distancias[actual] - 1:
                camino.append(vecino)
                break

    return camino[::-1]