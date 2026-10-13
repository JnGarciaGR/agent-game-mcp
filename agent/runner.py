import json

from groq import APIConnectionError, APITimeoutError, BadRequestError, RateLimitError
from langchain_core.messages import ToolMessage

from agent.prompt_message import PROMPT
from herramientas import ejecutar_accion
from time import perf_counter
from copy import deepcopy

def run_agent(modelo, estado, max_llamadas=5, on_step=None, stop_event=None,):
    inicio = perf_counter()
    mensajes = [
        ("system", PROMPT),
        (
            "human",
            "Completa la misión: recoge la llave, abre la puerta y llega "
            "a la salida. Primero observa la partida. Después utiliza "
            "el resultado para elegir tu siguiente acción.",
        ),
    ]

    llamadas = 0
    tokens_entrada = 0
    tokens_salida = 0
    historial = []   
    motivo_parada = "limite_llamadas"

    for turno in range(max_llamadas):
        if stop_event is not None and stop_event.is_set():
            motivo_parada = "cancelado"
            break
        if estado["terminado"]:
            break

        try:
            llamadas += 1
            respuesta = modelo.invoke(mensajes)
            # Cuenta el consumo aunque la respuesta no 
            # incluya una acción válida.
            uso = respuesta.usage_metadata or {}
            tokens_entrada += uso.get("input_tokens", 0)
            tokens_salida += uso.get("output_tokens", 0)
        except RateLimitError:
            print("Prueba detenida: se alcanzó un límite de uso de Groq.")
            motivo_parada = "limite_uso_groq"
            break
        except BadRequestError:
            print("Prueba detenida: Groq rechazó la solicitud o la llamada a herramienta.")
            motivo_parada = "solicitud_rechazada"
            break
        except APITimeoutError:
            motivo_parada = "tiempo_agotado"
            break
        except APIConnectionError:
            motivo_parada = "error_conexion"
            break

        if stop_event is not None and stop_event.is_set():
            motivo_parada = "cancelado"
            break

        if len(respuesta.tool_calls) != 1:
            print("Se detiene la prueba: se esperaba una herramienta.")
            print("Motivo:", respuesta.response_metadata.get("finish_reason"))
            motivo_parada = "respuesta_sin_accion_unica"
            print("Herramientas recibidas:", respuesta.tool_calls)
            print("Texto recibido:", respuesta.content)
            break

        llamada = respuesta.tool_calls[0]
        resultado = ejecutar_accion(
            estado, llamada["name"], **llamada["args"]
        )

        historial.append({
            "consulta": llamadas,
            "accion": llamada["name"],
            "argumentos": llamada["args"],
            "resultado": resultado,
            "posicion": estado["posicion_jugador"],
            "pasos": estado["pasos"],
        })

        # Notifica el estado tras la acción; no ejecuta el movimiento.
        # La copia conserva este momento sin compartir el estado original.
        if on_step is not None:
            on_step(deepcopy(estado))

        mensajes.append(respuesta)
        mensajes.append(
            ToolMessage(
                content=json.dumps(resultado, ensure_ascii=False),
                tool_call_id=llamada["id"],
            )
        )

        print(f"Consulta {turno + 1}: {llamada['name']} {llamada['args']}")
        if llamada["name"] != "observar":
            print("Resultado:", resultado["mensaje"])

    
        print("Posición:", estado["posicion_jugador"], "Pasos:", estado["pasos"])

    if estado["terminado"]:
        motivo_parada = "partida_terminada"

    return {
        "llamadas": llamadas,
        "pasos": estado["pasos"],
        "terminado": estado["terminado"],
        "motivo_fin": estado["motivo_fin"],
        "motivo_parada": motivo_parada,
        "historial": historial,
        "duracion_segundos": round(perf_counter() - inicio, 3),
        "semilla": estado["semilla"],
        "max_llamadas": max_llamadas,
        "max_pasos": estado["max_pasos"],
        "tokens_entrada": tokens_entrada,
        "tokens_salida": tokens_salida,
        "tokens_totales": tokens_entrada + tokens_salida,
    }
