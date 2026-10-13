PROMPT = """
Controlas un jugador en un laberinto por casillas.
Tu misión es recoger la llave, abrir la puerta y llegar a la salida.

El mapa usa estos símbolos:
# = pared, . = suelo, K = llave, D = puerta cerrada, S = salida.
La posición del jugador se proporciona por separado como (fila, columna).
Las coordenadas empiezan en cero. Las filas aumentan hacia abajo.

Usa las herramientas disponibles para observar, moverte, recoger y abrir.
Recoger requiere estar sobre la llave.
Abrir requiere tener la llave y señalar una puerta en una casilla vecina.

Solicita una sola acción por turno y revisa su resultado antes de continuar.
No supongas que una acción funcionó: comprueba la respuesta de la herramienta.
Evita repetir acciones fallidas sin cambiar tu estrategia.
Cuando la partida termine, no solicites más acciones.
"""