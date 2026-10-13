from estado import crear_estado_inicial


for semilla in range(100):
    estado = crear_estado_inicial(semilla)
    mapa = estado["mapa"]

    assert len(mapa) == 15, f"Altura incorrecta: {semilla}"
    assert all(len(fila) == 15 for fila in mapa), f"Ancho incorrecto: {semilla}"
    
    contenido = "".join(mapa)
    for simbolo in ("K", "D", "S"):
        assert contenido.count(simbolo) == 1, f"Cantidad de {simbolo}: {semilla}"

    repetido = crear_estado_inicial(semilla)
    assert estado == repetido, f"Resultado no reproducible: {semilla}"

print("Las 100 semillas pasaron las comprobaciones.")