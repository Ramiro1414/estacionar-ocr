import cv2
import numpy as np
import pytesseract

class ProcesadorPatente:
    def cargar_imagen(self, image_path):
        """Carga la imagen desde la ruta especificada."""
        image = cv2.imread(image_path)
        if image is None:
            print("Error: No se pudo cargar la imagen.")
        return image

    def convertir_a_grises(self, image):
        """Convierte la imagen a escala de grises."""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def aplicar_desenfoque(self, image):
        """Aplica desenfoque gaussiano para reducir el ruido."""
        return cv2.GaussianBlur(image, (5, 5), 0)

    def detectar_bordes(self, image):
        """Detecta bordes en la imagen utilizando el algoritmo de Canny."""
        return cv2.Canny(image, 75, 200)

    def encontrar_contornos(self, edges):
        """Encuentra contornos en la imagen a partir de los bordes detectados."""
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return sorted(contours, key=cv2.contourArea, reverse=True)

    def encontrar_patente(self, contours):
        """Intenta encontrar un contorno que represente la patente de un vehículo."""
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4:
                return approx
        return None

    def ordenar_puntos(self, points):
        """Ordena las esquinas de un polígono."""
        rect = np.zeros((4, 2), dtype="float32")
        s = points.sum(axis=1)
        rect[0] = points[np.argmin(s)]
        rect[2] = points[np.argmax(s)]
        diff = np.diff(points, axis=1)
        rect[1] = points[np.argmin(diff)]
        rect[3] = points[np.argmax(diff)]
        return rect

    def transformar_perspectiva(self, image, rect):
        """Aplica la transformación de perspectiva para enderezar la imagen."""
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        return cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    def aplicar_ocr(self, image):
        """Aplica OCR a la imagen enderezada para extraer la patente."""
        custom_config = r'--oem 3 --psm 6'
        texto = pytesseract.image_to_string(image, config=custom_config)
        texto_procesado = texto.replace(" ", "").upper()
        return texto_procesado.strip()

    def procesar_imagen(self, image_path):
        """Función principal para procesar la imagen y enderezarla."""
        image = self.cargar_imagen(image_path)
        if image is None:
            return None

        gray_image = self.convertir_a_grises(image)
        blurred_image = self.aplicar_desenfoque(gray_image)
        edges = self.detectar_bordes(blurred_image)
        contours = self.encontrar_contornos(edges)
        screen_contour = self.encontrar_patente(contours)

        if screen_contour is not None:
            rect = self.ordenar_puntos(screen_contour.reshape(4, 2))
            warped_image = self.transformar_perspectiva(image, rect)
            cv2.imwrite("../imagen_patente_preprocesada/imagen-procesada.png", warped_image)
            patente = self.aplicar_ocr(warped_image)
            return patente 
        else:
            return None

