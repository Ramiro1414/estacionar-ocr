import unittest

from apps.proceso_reconocimiento_patentes import ProcesadorPatente

class TestDeteccionPatente(unittest.TestCase):

    def setUp(self):
        self.procesador = ProcesadorPatente()

    def test_deteccion_patente_1(self):
        imagen_test_pasa_1 = "/home/alan/detector_patentes/imagenes_test/imagen_test_pasa_1.png"
       
        patente_resultado_1 = self.procesador.procesar_imagen(imagen_test_pasa_1)
        print("Imagen procesada 1: ", patente_resultado_1)
       
        self.assertEqual(patente_resultado_1, "AB123CD")

    def test_deteccion_patente_2(self):
        imagen_test_pasa_2 = "/home/alan/detector_patentes/imagenes_test/imagen_test_pasa_2.png"

        patente_resultado_2 = self.procesador.procesar_imagen(imagen_test_pasa_2)
        print("Imagen procesada 2: ", patente_resultado_2)

        self.assertEqual(patente_resultado_2, "SBZ7971")

    def test_deteccion_patente_none(self):

        imagen_test_no_pasa = "/home/alan/detector_patentes/imagenes_test/imagen_test_no_pasa.png"

        patente_resultado_3 = self.procesador.procesar_imagen(imagen_test_no_pasa)
        print("Imagen procesada 3: ", patente_resultado_3)

        self.assertEqual(patente_resultado_3, None)

if __name__ == "__main__":
    unittest.main()
