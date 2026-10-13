import pygame

from estado import crear_estado_inicial
from acciones import mover, recoger, abrir, ha_ganado
from queue import Empty
from agent.visual_bridge import crear_canal
from agent.background import iniciar_agente
from agent.modelo import create_agent_model
TAMANO_CASILLA = 26
MARGEN = 24

COLORES = {
    "#": (75, 85, 105),    # Pared
    ".": (35, 42, 55),     # Suelo
    "K": (245, 200, 60),   # Llave
    "D": (155, 95, 50),    # Puerta
    "S": (65, 185, 115),   # Salida
}

MOTIVOS_PARADA = {
    "limite_llamadas": "Límite de consultas",
    "limite_uso_groq": "Cuota de Groq",
    "solicitud_rechazada": "Solicitud rechazada",
    "respuesta_sin_accion_unica": "Respuesta no válida",
    "partida_terminada": "Partida terminada",
    "cancelado": "Cancelado",
    "tiempo_agotado": "Tiempo agotado",
    "error_conexion": "Error de conexión",
}

direcciones_por_tecla = {
        pygame.K_UP: "arriba",
        pygame.K_DOWN: "abajo",
        pygame.K_LEFT: "izquierda",
        pygame.K_RIGHT: "derecha",
}

def dibujar_tablero(pantalla, estado, fuente):
    for fila, contenido in enumerate(estado["mapa"]):
        for columna, simbolo in enumerate(contenido):
            x = MARGEN + columna * TAMANO_CASILLA
            y = MARGEN + fila * TAMANO_CASILLA

            casilla = pygame.Rect(
                x, y, TAMANO_CASILLA - 2, TAMANO_CASILLA - 2
            )
            pygame.draw.rect(pantalla, COLORES[simbolo], casilla)

            if simbolo in ("K", "D", "S"):
                texto = fuente.render(simbolo, True, (20, 20, 25))
                pantalla.blit(texto, texto.get_rect(center=casilla.center))

    fila, columna = estado["posicion_jugador"]
    centro = (
        MARGEN + columna * TAMANO_CASILLA + TAMANO_CASILLA // 2,
        MARGEN + fila * TAMANO_CASILLA + TAMANO_CASILLA // 2,
    )
    pygame.draw.circle(pantalla, (80, 170, 255), centro, 9)


def iniciar_ventana(modo_agente=True):
    pygame.init()

    pantalla = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Game Agent MCP")
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 24)
    estado = crear_estado_inicial()
    actualizaciones, publicar_estado = crear_canal()
    detener = None
    resumen_agente = None

    if modo_agente:
        modelo = create_agent_model()
        hilo, detener, resultados = iniciar_agente(
            modelo, estado, publicar_estado
        )
    
    ejecutando = True
    ultima_direccion = "abajo"
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if detener is not None:
                    detener.set()
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and not modo_agente:
                direccion = direcciones_por_tecla.get(evento.key)
                if direccion is not None:
                    ultima_direccion = direccion
                    resultado = mover(estado, direccion)
                    print(resultado["mensaje"])
                    if resultado["exito"] and ha_ganado(estado):
                        print("¡Misión completada!")
                elif evento.key == pygame.K_e:
                    resultado = recoger(estado)
                    print(resultado["mensaje"])
                elif evento.key == pygame.K_o:
                    resultado = abrir(estado, ultima_direccion)
                    print(resultado["mensaje"])
        try:
            estado = actualizaciones.get_nowait()
        except Empty:
            pass
        if modo_agente and resumen_agente is None:
            try:
                resumen_agente = resultados.get_nowait()
                print("Motivo de parada:", resumen_agente["motivo_parada"])
            except Empty:
                pass
        pantalla.fill((25, 30, 40))
        dibujar_tablero(pantalla, estado, fuente)
        texto_semilla = fuente.render(
            f"Semilla: {estado['semilla']}", True, (220, 225, 235)
        )
        pantalla.blit(texto_semilla, (MARGEN, 436))
        
        texto_pasos = fuente.render(
            f"Pasos: {estado['pasos']}/{estado['max_pasos']}",
            True, (220, 225, 235)
        )
        pantalla.blit(texto_pasos, (440, 24))

        if estado["terminado"]:
            if estado["motivo_fin"] == "victoria":
                mensaje = "¡Victoria!"
            else:
                mensaje = "Límite agotado"

            texto_resultado = fuente.render(
                mensaje, True, (245, 200, 60)
            )
            pantalla.blit(texto_resultado, (440, 60))

        if modo_agente:
            mensaje_agente = (
                "Agente activo" if hilo.is_alive() else "Agente detenido"
            )
            texto_agente = fuente.render(
                mensaje_agente, True, (220, 225, 235)
            )
            pantalla.blit(texto_agente, (440, 100))

        if modo_agente and resumen_agente is not None:
            motivo = resumen_agente["motivo_parada"]
            mensaje = MOTIVOS_PARADA.get(motivo, "Motivo desconocido")
            texto_motivo = fuente.render(
                mensaje, True, (245, 200, 60)
            )
            pantalla.blit(texto_motivo, (440, 130))

        pygame.display.flip()
        reloj.tick(60)


    pygame.quit()
