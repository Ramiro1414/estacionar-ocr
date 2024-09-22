# main.py
from proceso_reconocimiento_patentes import ProcesadorPatente

def main():
    procesador = ProcesadorPatente()
    imagen_path = "/home/alan/detector_patentes/imagenes_patentes/auto-patente1.png"
    patente = procesador.procesar_imagen(imagen_path)
    
    if patente:
        print("Patente detectada:", patente)
    else:
        print("No se pudo detectar la patente.")

if __name__ == "__main__":
    main()
 