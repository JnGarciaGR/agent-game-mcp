from queue import Queue


def crear_canal():
    actualizaciones = Queue()

    def publicar_estado(estado):
        actualizaciones.put(estado)

    return actualizaciones, publicar_estado