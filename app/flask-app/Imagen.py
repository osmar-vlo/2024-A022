import cv2

class Imagen:

    def __init__(self, img):
            self.imagen = cv2.imread(img, cv2.IMREAD_COLOR)
            #self.imagen = cv2.imdecode(img, cv2.IMREAD_COLOR)
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
            cascada_rostros = cv2.CascadeClassifier('./resources/haarcascade_frontalface_default.xml')

            # Detectar rostros en la imagen en escala de grises
            rostros = cascada_rostros.detectMultiScale(imagen_gris, scaleFactor=1.3, minNeighbors=5)

            margen = 20 # Margen adicional alrededor del rostro
            # Iterar sobre los rostros detectados
            for i, (x, y, w, h) in enumerate(rostros):
                # Calcular nuevas coordenadas de recorte centradas
                nuevo_x = max(0, x - margen)
                nuevo_y = max(0, y - margen)
                nuevo_w = min(imagen_gris.shape[1] - nuevo_x, w + 2 * margen)
                nuevo_h = min(imagen_gris.shape[0] - nuevo_y, h + 2 * margen)
                # ROI en escala de grises
                roi_gris = imagen_gris[nuevo_y:nuevo_y+nuevo_h, nuevo_x:nuevo_x+nuevo_w]
                gris_roi_resized = cv2.resize(roi_gris, (300, 300), interpolation=cv2.INTER_LANCZOS4)
                cv2.imwrite(f"roi_{i}.png", gris_roi_resized)
                self.gris_roi.append(gris_roi_resized)

                # ROI en color
                roi_color = imagen_lan[y:y+h, x:x+w]
                self.color_roi.append(cv2.resize(roi_color, (300, 300), interpolation=cv2.INTER_LANCZOS4))
            
            # Devolver
            return self.gris_roi, self.color_roi

        except Exception as e:
            # Manejo de errores
            print(f"Error en la detección facial: {e}")