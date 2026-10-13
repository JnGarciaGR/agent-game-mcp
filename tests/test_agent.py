import unittest
from unittest.mock import patch

import httpx
from groq import RateLimitError, BadRequestError

from agent.model_test import main


class PruebasErroresAgente(unittest.TestCase):
    @patch("agent.model_test.create_agent_model")
    def test_limite_groq_detiene_consultas(self, crear_modelo):
        cliente = crear_modelo.return_value
        respuesta = httpx.Response(
            429,
            request=httpx.Request("POST", "https://example.test"),
        )
        cliente.invoke.side_effect = RateLimitError(
            "Límite simulado",
            response=respuesta,
            body=None,
        )

        with patch(
            "agent.model_test.guardar_resultado",
            return_value="archivo_simulado.json",
        ):
            main()

        cliente.invoke.assert_called_once()

    @patch("agent.model_test.create_agent_model")
    def test_solicitud_invalida_detiene_consultas(self, crear_modelo):
        cliente = crear_modelo.return_value
        respuesta = httpx.Response(
            400,
            request=httpx.Request("POST", "https://example.test"),
        )
        cliente.invoke.side_effect = BadRequestError(
            "Llamada a herramienta inválida",
            response=respuesta,
            body={"code": "tool_use_failed"},
        )

        with patch(
            "agent.model_test.guardar_resultado",
            return_value="archivo_simulado.json",
        ):
            main()

        cliente.invoke.assert_called_once()

    