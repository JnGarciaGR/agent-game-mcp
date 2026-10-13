import random


def variar_llave(mapa, semilla=None):
    azar = random.Random(semilla)
    nuevo_mapa = [list(fila.replace("K", ".")) for fila in mapa]

    posiciones = []

    for fila in range(1, 6):
        for columna in range(1, 8):
            if nuevo_mapa[fila][columna] == "." and (fila, columna) != (1, 1):
                posiciones.append((fila, columna))

    fila, columna = azar.choice(posiciones)
    nuevo_mapa[fila][columna] = "K"

    return ["".join(fila) for fila in nuevo_mapa]

def variar_salida(mapa, semilla=None):
    azar = random.Random(semilla)
    nuevo_mapa = [list(fila.replace("S", ".")) for fila in mapa]

    columna = azar.randint(1, 7)
    nuevo_mapa[7][columna] = "S"

    return ["".join(fila) for fila in nuevo_mapa]

def variar_puerta(mapa, semilla=None):
    azar = random.Random(semilla)
    nuevo_mapa = [list(fila.replace("D", "#")) for fila in mapa]

    columna = azar.randint(1, 7)
    nuevo_mapa[6][columna] = "D"

    return ["".join(fila) for fila in nuevo_mapa]

def variar_pasillos(mapa, semilla=None):
    azar = random.Random(semilla)
    nuevo_mapa = mapa.copy()

    if azar.choice([True, False]):
        for fila in range(2, 5):
            nuevo_mapa[fila] = nuevo_mapa[fila][::-1]

    return nuevo_mapa