import unittest

from apps.proceso_deteccion_texto_plano import ProcesadorTextoPlano

class TestDeteccionPatente(unittest.TestCase):

    def setUp(self):
        self.procesador = ProcesadorTextoPlano()

    def test_deteccion_patente(self):
        imagen_test_pasa_1 = "/home/alan/ocr-estacionar/imagenes_test/textoplano.png"
        
        texto_detectado = self.procesador.procesar_imagen(imagen_test_pasa_1)
        print("Texto detectado:\n", texto_detectado)

        self.assertEqual(texto_detectado, "Hola Mundo\nEsto es un texto plano y binario")

if __name__ == "__main__":
    unittest.main()
