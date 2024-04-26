import cv2

class Imagen:

    def __init__(self, img):
            self.imagen = cv2.imread(img)
            self.gris_roi = []
            self.color_roi = []
        
    def preprocesamiento(self):
        try:
            # Redimensionar la imagen con interpolación (interpolación Lanczos)
            imagen_lan = cv2.resize(self.imagen, (600, 600), interpolation=cv2.INTER_LANCZOS4)

            # Convertir la imagen a escala de grises
            imagen_gris = cv2.cvtColor(imagen_lan, cv2.COLOR_BGR2GRAY)

            # Devolver la imagen en escala de grises
            return imagen_lan, imagen_gris
        
        except Exception as e:
            # Manejo de errores
            print(f"Error en el preprocesamiento: {e}")

    def deteccion_facial(self, imagen_lan, imagen_gris):
        try:
            # Cargar el clasificador OpenCV
            cascada_rostros = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            # Detectar rostros en la imagen en escala de grises
            rostros = cascada_rostros.detectMultiScale(imagen_gris, scaleFactor=1.3, minNeighbors=5)

            # Iterar sobre los rostros detectados
            for i, (x, y, w, h) in enumerate(rostros):
                # Calcular la posición vertical ajustada
                ajuste_vertical = 150 
                y_ajustado = max(y - ajuste_vertical, 200)

                # ROI en escala de grises
                roi_gris = imagen_gris[y:y+h, x:x+w]
                self.gris_roi.append(cv2.resize(roi_gris, (300, 300), interpolation=cv2.INTER_LANCZOS4))

                # ROI en color
                roi_color = imagen_lan[y:y+h, x:x+w]
                self.color_roi.append(cv2.resize(roi_color, (300, 300), interpolation=cv2.INTER_LANCZOS4))
            
            # Devolver
            return self.gris_roi, self.color_roi

        except Exception as e:
            # Manejo de errores
            print(f"Error en la detección facial: {e}")