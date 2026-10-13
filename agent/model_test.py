from agent.modelo import create_agent_model
from agent.runner import run_agent
from estado import crear_estado_inicial
from agent.registros import guardar_resultado

def main():
    modelo = create_agent_model()
    estado = crear_estado_inicial(42)
    resumen = run_agent(modelo, estado)
    ruta = guardar_resultado(resumen)
    print("Resultado guardado en:", ruta)
    print("Acciones registradas:", len(resumen["historial"]))
    for registro in resumen["historial"]:
        print(registro)

if __name__ == "__main__":
    main()