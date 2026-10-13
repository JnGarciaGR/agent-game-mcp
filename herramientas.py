from acciones import observar, mover, recoger, abrir


def ejecutar_accion(estado, accion, direccion=None):
    if accion == "observar":
        return observar(estado)

    if accion == "mover":
        return mover(estado, direccion)

    if accion == "recoger":
        return recoger(estado)

    if accion == "abrir":
        return abrir(estado, direccion)

    return {"exito": False, "mensaje": "Acción desconocida."}