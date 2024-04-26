import cv2

from Imagen import Imagen
from Rostro import Rostro

# Crear una instancia de la clase Imagen
imagen = Imagen('prueba.jpg')

# Realizar el preprocesamiento y obtener las imágenes procesadas
imagen_lan, imagen_gris = imagen.preprocesamiento()

# Realizar la detección facial y obtener los ROIs
gris_rois, color_rois = imagen.deteccion_facial(imagen_lan, imagen_gris)

# Crear una instancia de la clase Rostro
rostro = Rostro()

# Iterar sobre los ROIs y guardarlos como imágenes
for i, (roi_gris, roi_color) in enumerate(zip(gris_rois, color_rois)):
    rostro.get_landmarks_image(roi_gris, roi_color)