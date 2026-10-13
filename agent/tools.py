TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "observar",
            "description": (
                "Consulta el mapa, la posición del jugador, el inventario, "
                "los pasos disponibles y si la partida terminó."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mover",
            "description": (
                "Intenta mover al jugador una casilla en la dirección indicada. "
                "Las paredes y las puertas cerradas bloquean el movimiento. "
                "El intento consume un paso aunque el movimiento falle."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    # Entrada de mover(): type define el tipo y enum los valores permitidos.
                    "direccion": {
                        "type": "string",
                        "enum": ["arriba", "abajo", "izquierda", "derecha"],
                        "description": "Dirección del movimiento.",
                    },
                },
                "required": ["direccion"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "recoger",
            "description": (
                "Recoge la llave si el jugador está sobre su casilla. "
                "El intento consume un paso aunque falle."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "abrir",
            "description": (
                "Abre una puerta en la casilla vecina indicada. "
                "Requiere haber recogido la llave. No mueve al jugador. "
                "El intento consume un paso aunque falle."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "direccion": {
                        "type": "string",
                        "enum": ["arriba", "abajo", "izquierda", "derecha"],
                        "description": "Dirección donde está la puerta.",
                    },
                },
                "required": ["direccion"],
            },
        },
    },

]
