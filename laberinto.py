import random
from validacion import calcular_distancias, casillas_alcanzables, reconstruir_camino
def crear_base(tamano=15):
    if tamano < 5 or tamano % 2 == 0:
        raise ValueError("El tamaño debe ser impar y al menos 5.")

    mapa = [
        ["#"] * tamano
        for _ in range(tamano)
    ]
    mapa[1][1] = "."

    return mapa

def vecinos_sin_excavar(mapa, posicion):
    fila, columna = posicion
    candidatos = []

    for cambio_fila, cambio_columna in [
        (-2, 0), (2, 0), (0, -2), (0, 2)
    ]:
        nueva_fila = fila + cambio_fila
        nueva_columna = columna + cambio_columna

        if 0 < nueva_fila < len(mapa) - 1:
            if 0 < nueva_columna < len(mapa[0]) - 1:
                if mapa[nueva_fila][nueva_columna] == "#":
                    candidatos.append((nueva_fila, nueva_columna))

    return candidatos

def excavar_paso(mapa, origen, destino):
    fila_origen, columna_origen = origen
    fila_destino, columna_destino = destino

    fila_intermedia = (fila_origen + fila_destino) // 2
    columna_intermedia = (columna_origen + columna_destino) // 2

    mapa[fila_intermedia][columna_intermedia] = "."
    mapa[fila_destino][columna_destino] = "."

def excavar_un_paso(mapa, origen, azar):
    candidatos = vecinos_sin_excavar(mapa, origen)

    if not candidatos:
        return None

    destino = azar.choice(candidatos)
    excavar_paso(mapa, origen, destino)

    return destino

def generar_laberinto(tamano=15, semilla=None):
    azar = random.Random(semilla)
    mapa = crear_base(tamano)
    camino = [(1, 1)]

    while camino:
        origen = camino[-1]
        destino = excavar_un_paso(mapa, origen, azar)

        if destino is None:
            camino.pop()
        else:
            camino.append(destino)

    return ["".join(fila) for fila in mapa]

def colocar_salida(mapa, inicio=(1, 1)):
    distancias = calcular_distancias(mapa, inicio)
    posicion_salida = max(distancias, key=distancias.get)

    fila, columna = posicion_salida
    nuevo_mapa = mapa.copy()
    contenido = nuevo_mapa[fila]
    nuevo_mapa[fila] = contenido[:columna] + "S" + contenido[columna + 1:]

    return nuevo_mapa

def colocar_puerta(mapa, camino, separacion=8):
    indice = min(len(camino) // 2, len(camino) - 1 - separacion)

    if indice < 1:
        raise ValueError("El camino es demasiado corto para colocar la puerta.")

    fila, columna = camino[indice]
    nuevo_mapa = mapa.copy()
    contenido = nuevo_mapa[fila]
    nuevo_mapa[fila] = contenido[:columna] + "D" + contenido[columna + 1:]

    return nuevo_mapa

def colocar_llave(mapa, camino, semilla=None):
    azar = random.Random(semilla)
    alcanzables = casillas_alcanzables(mapa, camino[0])
    candidatos = []

    for posicion in sorted(alcanzables):
        if posicion not in camino:
            candidatos.append(posicion)

    if not candidatos:
        raise ValueError("Este laberinto no tiene un desvío para la llave.")

    fila, columna = azar.choice(candidatos)
    nuevo_mapa = mapa.copy()
    contenido = nuevo_mapa[fila]
    nuevo_mapa[fila] = contenido[:columna] + "K" + contenido[columna + 1:]

    return nuevo_mapa

def generar_escenario(semilla=None):
    inicio = (1, 1)
    mapa = generar_laberinto(15, semilla)

    distancias = calcular_distancias(mapa, inicio)
    salida = max(distancias, key=distancias.get)
    camino = reconstruir_camino(mapa, inicio, salida)

    mapa = colocar_salida(mapa, inicio)
    mapa = colocar_puerta(mapa, camino)
    mapa = colocar_llave(mapa, camino, semilla)

    return mapa

def generar_con_reintentos(semilla, max_intentos=20):
    for intento in range(max_intentos):
        semilla_actual = semilla + intento

        try:
            mapa = generar_escenario(semilla_actual)
        except ValueError:
            continue

        return mapa, semilla_actual

    raise ValueError(
        f"No se pudo generar un escenario en {max_intentos} intentos."
    )