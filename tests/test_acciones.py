import unittest

from acciones import mover


class PruebasFinalizacion(unittest.TestCase):
    def test_victoria_bloquea_movimiento(self):
        estado = {
            "mapa": ["#####", "#.S##", "#####"],
            "posicion_jugador": (1, 1),
            "terminado": False,
            "motivo_fin": None,
            "pasos": 0,
            "max_pasos": 10,
        }

        resultado = mover(estado, "derecha")

        self.assertTrue(resultado["exito"])
        self.assertTrue(estado["terminado"])
        self.assertEqual(estado["motivo_fin"], "victoria")

        resultado = mover(estado, "izquierda")

        self.assertFalse(resultado["exito"])
        self.assertEqual(estado["posicion_jugador"], (1, 2))
        self.assertEqual(estado["pasos"], 1)

    def test_victoria_en_ultimo_paso(self):
        estado = {
            "mapa": ["#####", "#.S##", "#####"],
            "posicion_jugador": (1, 1),
            "terminado": False,
            "motivo_fin": None,
            "pasos": 0,
            "max_pasos": 1,
        }

        resultado = mover(estado, "derecha")

        self.assertTrue(resultado["exito"])
        self.assertTrue(estado["terminado"])
        self.assertEqual(estado["motivo_fin"], "victoria")
        self.assertEqual(estado["pasos"], 1)

    def test_limite_bloquea_nuevas_acciones(self):
        estado = {
            "mapa": ["######", "#..S##", "######"],
            "posicion_jugador": (1, 1),
            "terminado": False,
            "motivo_fin": None,
            "pasos": 0,
            "max_pasos": 1,
        }

        resultado = mover(estado, "derecha")

        self.assertTrue(resultado["exito"])
        self.assertTrue(estado["terminado"])
        self.assertEqual(estado["motivo_fin"], "limite_pasos")

        resultado = mover(estado, "derecha")

        self.assertFalse(resultado["exito"])
        self.assertEqual(estado["posicion_jugador"], (1, 2))
        self.assertEqual(estado["pasos"], 1)