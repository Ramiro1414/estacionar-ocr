import cv2
import pytesseract

class ProcesadorTextoPlano:
    def cargar_imagen(self, image_path):
        # Carga la imagen desde la ruta especificada.
        image = cv2.imread(image_path)
        if image is None:
            print("Error: No se pudo cargar la imagen.")
            return None
        return image

    def aplicar_ocr(self, image):
        # Aplica OCR a la imagen binarizada para extraer el texto.
        custom_config = r'--oem 3 --psm 6'
        texto = pytesseract.image_to_string(image, config=custom_config)
        return texto.strip()

    def procesar_imagen(self, image_path):
        # Función principal para cargar, preprocesar y aplicar OCR a la imagen.
        image = self.cargar_imagen(image_path)
        if image is None:
            return
        
        texto_detectado = self.aplicar_ocr(image)
        return texto_detectado
