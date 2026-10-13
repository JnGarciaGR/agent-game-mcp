from copy import deepcopy
from threading import Event, Thread
from queue import Queue
from agent.registros import guardar_resultado
from agent.runner import run_agent


def iniciar_agente(modelo, estado, publicar_estado):
    detener = Event()
    resultados = Queue()
    estado_agente = deepcopy(estado)

    def trabajar():
        resumen = run_agent(
            modelo,
            estado_agente,
            max_llamadas=5,
            on_step=publicar_estado,
            stop_event=detener,
        )
        resultados.put(resumen)
        ruta = guardar_resultado(resumen)
        print("Resultado guardado en:", ruta)

    hilo = Thread(target=trabajar)
    hilo.start()

    return hilo, detener, resultados