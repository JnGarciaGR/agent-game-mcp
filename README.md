# Game Agent MCP

Entorno de experimentación para agentes de IA en un laberinto desarrollado con Python y Pygame. El agente debe recoger una llave, abrir una puerta y alcanzar la salida dentro de un límite de acciones.

El objetivo es evaluar cómo un modelo de lenguaje utiliza herramientas, interpreta los resultados y ajusta sus decisiones. El proyecto contempla escenarios reproducibles, ejecución visual, registro de métricas e integración con Model Context Protocol (MCP).

**Estado actual:** integración funcional entre el juego y un modelo servido por Groq. La ejecución visual está limitada a cinco consultas por partida. La integración con MCP y la evaluación sistemática siguen pendientes.

## Arquitectura

El proyecto separa las reglas del entorno, la ejecución del agente y la presentación:

| Componente | Responsabilidad |
| --- | --- |
| `estado.py`, `acciones.py` | Estado, movimientos, inventario y condiciones de finalización. |
| `laberinto.py`, `validacion.py` | Generación de escenarios y validación de accesibilidad. |
| `herramientas.py` | Despacho de las acciones solicitadas por el agente. |
| `agent/tools.py`, `agent/modelo.py` | Definición de herramientas y configuración de `ChatGroq` mediante LangChain. |
| `agent/runner.py` | Ciclo de consultas, ejecución de herramientas, historial y límites. |
| `agent/background.py`, `agent/visual_bridge.py` | Hilo de ejecución, cancelación y comunicación con la interfaz mediante colas. |
| `vista.py`, `game.py` | Renderizado, eventos de Pygame y punto de entrada. |
| `agent/registros.py` | Persistencia del resumen y del historial en JSON. |

### Flujo del agente

1. El modelo recibe las instrucciones de la misión y las definiciones de `observar`, `mover`, `recoger` y `abrir`.
2. Cada respuesta debe contener una única llamada a herramienta. El programa ejecuta la acción sobre el estado de la partida.
3. La respuesta del modelo y el resultado de la herramienta se incorporan a la conversación mediante `ToolMessage`.
4. El modelo utiliza ese resultado en su siguiente decisión. El ciclo termina al finalizar la partida, alcanzar un límite, recibir una respuesta no válida o detectar un error controlado.

`observar` proporciona el mapa completo y el estado del jugador. Las herramientas se ejecutan localmente desde Python; la capa MCP todavía no está implementada.

El agente trabaja sobre una copia del estado en un hilo independiente. Después de cada acción, un callback publica una copia del estado actualizado en una cola. Pygame consume esas actualizaciones desde su bucle principal sin bloquearse durante las consultas al modelo.

## Escenarios y registros

Los mapas actuales son de **15 × 15** casillas y se generan mediante búsqueda en profundidad con retroceso. La salida se sitúa en una posición de máxima distancia desde el inicio; la puerta bloquea el recorrido hacia ella y la llave se ubica en un desvío accesible antes de abrirla.

La generación utiliza semillas y valida las condiciones de la misión. Si un escenario no admite la colocación de los elementos, se prueban semillas consecutivas, con un máximo de 20 intentos. El registro conserva la semilla utilizada.

Cada ejecución guarda un archivo `resultados/partida_<id>.json` con acciones, argumentos, resultados, posiciones, consultas, pasos, duración, tokens reportados, semilla, límites y motivos de parada. El historial se persiste para su análisis; la conversación enviada al modelo se mantiene en memoria durante la partida.

## Fases de desarrollo

| Fase | Alcance | Estado |
| --- | --- | --- |
| 1. Entorno | Reglas, interfaz Pygame y finalización de partidas. | Implementada |
| 2. Generación | Laberintos reproducibles y validación de la misión. | Implementada |
| 3. Agente | Integración con Groq, llamadas a herramientas y ejecución visual. | Primera versión funcional |
| 4. Control y registro | Límites, cancelación, manejo de errores y persistencia de resultados. | Base implementada |
| 5. Evaluación | Ampliar partidas, controlar la frecuencia de consultas y medir victorias, acciones inválidas, repeticiones y consumo en distintas semillas. | Pendiente |
| 6. Interfaz | Mostrar la última acción y su resultado, e iniciar nuevas partidas desde la ventana. | Pendiente |
| 7. MCP | Publicar las herramientas mediante un servidor MCP y conectarlas con clientes compatibles. | Pendiente |

## Configuración y ejecución

Entorno de desarrollo: **Python 3.12 y Pygame 2.6.1**. La integración utiliza `langchain-groq`, `langchain-core`, `groq` y `python-dotenv`. El proyecto aún no incluye un archivo de dependencias con versiones fijadas.

Con el entorno virtual y las dependencias instaladas, copia `.env.example` como `.env` y configura `GROQ_API_KEY` y `GROQ_MODEL`. El archivo `.env` y los resultados de las partidas están excluidos de Git.

```powershell
# Ejecución visual
python game.py

# Ejecución del agente en consola
python -m agent.model_test
```

La configuración del modelo está en `agent/modelo.py`: temperatura `0`, esfuerzo de razonamiento `low`, máximo de salida de `2048` tokens, timeout de `30` segundos y reintentos automáticos desactivados. El modelo seleccionado debe admitir las herramientas y los parámetros configurados.

## Pruebas

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python seed_check.py
```

Las pruebas unitarias cubren condiciones de finalización y errores simulados de Groq, sin consultar la API. `seed_check.py` comprueba dimensiones, elementos únicos y reproducibilidad para 100 semillas de entrada, además de la validación realizada al crear cada estado.

## Limitaciones actuales

- El límite de cinco consultas permite comprobar la integración, pero no evaluar recorridos completos. Es independiente del límite de 300 pasos del juego.
- El agente puede repetir movimientos, intentar atravesar paredes o responder sin una acción válida. Su tasa de éxito aún no se ha medido.
- El consumo de tokens se registra, pero todavía no se aplica un presupuesto de tokens por partida ni un control de frecuencia de solicitudes.
- La cancelación se comprueba entre consultas y después de recibir una respuesta; no interrumpe una petición de red en curso.
- La ventana permanece abierta al detenerse el agente para permitir revisar el estado final.
