import cv2
import dlib
import base64
import math

class Rostro:

    def __init__(self, gris_cuts, color_cuts):
            self.gris_cuts = gris_cuts
            self.color_cuts = color_cuts
            self.landmarks = [] 
            self.dist_ojo_der = []
            self.dist_ojo_izq = []
            self.dist_ceja_der = []
            self.dist_ceja_izq = []
            self.dist_nariz = []
            self.dist_forma = []

    def get_landmarks_image(self):
        try:
            # Cargar el detector de caras de dlib (HOG-based)
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor("./resources/shape_predictor_68_face_landmarks.dat")        
            # Iterar sobre las imágenes en escala de grises y en color
            
            for imagen_gris, imagen_color in zip(self.gris_cuts, self.color_cuts):
                caras = detector(imagen_gris)
                for cara in caras:
                    landmarks = predictor(imagen_gris, cara)
                    # Crear una copia de la imagen a color para dibujar las landmarks
                    imagen_color_con_landmarks = imagen_color.copy()
                    ojo_izq = []
                    ojo_der = []
                    ceja_izq = []
                    ceja_der = []
                    nariz = []
                    forma = []
                    # Forma del rostro
                    for n in range(0, 17):
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        cv2.circle(imagen_color_con_landmarks, (x, y), 2, (0, 255, 0), -1)  # Dibujar un círculo verde
                        # Mostrar el número de landmark
                        cv2.putText(imagen_color_con_landmarks, str(n), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
                        forma.append((x, y))  # Guardar los puntos de la forma del rostro
                    # Ceja derecha
                    for n in range(17, 22):
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        cv2.circle(imagen_color_con_landmarks, (x, y), 2, (0, 0, 255), -1)  # Dibujar un círculo rojo
                        # Mostrar el número de landmark
                        cv2.putText(imagen_color_con_landmarks, str(n), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
                        ceja_der.append((x, y))  # Guardar los puntos de la ceja derecha
                    # Ceja izquierda
                    for n in range(22, 27):
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        cv2.circle(imagen_color_con_landmarks, (x, y), 2, (255, 0, 0), -1)  # Dibujar un círculo azul
                        # Mostrar el número de landmark
                        cv2.putText(imagen_color_con_landmarks, str(n), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
                        ceja_izq.append((x, y))  # Guardar los puntos de la ceja izq
                    # Nariz
                    for n in range(27, 36):
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        cv2.circle(imagen_color_con_landmarks, (x, y), 2, (255, 255, 0), -1)  # Dibujar un círculo cyan
                        # Mostrar el número de landmark
                        cv2.putText(imagen_color_con_landmarks, str(n), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
                        nariz.append((x, y))  # Guardar los puntos de la nariz
                    # Ojo derecho
                    for n in range(36, 42):
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        cv2.circle(imagen_color_con_landmarks, (x, y), 2, (0, 255, 255), -1)  # Dibujar un círculo amarillo
                        # Mostrar el número de landmark
                        cv2.putText(imagen_color_con_landmarks, str(n), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
                        ojo_der.append((x, y))  # Guardar los puntos del ojo derecho
                    # Ojo izquierdo
                    for n in range(42, 48):
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        cv2.circle(imagen_color_con_landmarks, (x, y), 2, (255, 0, 255), -1)  # Dibujar un círculo rosa
                        # Mostrar el número de landmark
                        cv2.putText(imagen_color_con_landmarks, str(n), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
                        ojo_izq.append((x, y))  # Guardar los puntos del ojo derecho
                    for n in range(48, 68):
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        cv2.circle(imagen_color_con_landmarks, (x, y), 2, (150, 150, 0), -1)  # Dibujar un círculo azul menta
                        # Mostrar el número de landmark
                        cv2.putText(imagen_color_con_landmarks, str(n), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
                    # Calcular la distancia euclidiana.
                    distancia_ojo_der = [math.sqrt((ojo_der[i][0] - ojo_der[i+1][0])**2 + (ojo_der[i][1] - ojo_der[i+1][1])**2) for i in range(len(ojo_der)-1)]
                    distancia_ojo_izq = [math.sqrt((ojo_izq[i][0] - ojo_izq[i+1][0])**2 + (ojo_izq[i][1] - ojo_izq[i+1][1])**2) for i in range(len(ojo_izq)-1)]
                    distancia_ceja_der = [math.sqrt((ceja_der[i][0] - ceja_der[i+1][0])**2 + (ceja_der[i][1] - ceja_der[i+1][1])**2) for i in range(len(ceja_der)-1)]
                    distancia_ceja_izq = [math.sqrt((ceja_izq[i][0] - ceja_izq[i+1][0])**2 + (ceja_izq[i][1] - ceja_izq[i+1][1])**2) for i in range(len(ceja_izq)-1)]
                    distancia_nariz = [math.sqrt((nariz[i][0] - nariz[i+1][0])**2 + (nariz[i][1] - nariz[i+1][1])**2) for i in range(len(nariz)-1)]
                    distancia_forma = [math.sqrt((forma[i][0] - forma[i+1][0])**2 + (forma[i][1] - forma[i+1][1])**2) for i in range(len(forma)-1)]
                    # Guardar las distancias calculadas
                    self.dist_ojo_der.append(distancia_ojo_der)
                    self.dist_ojo_izq.append(distancia_ojo_izq)
                    self.dist_ceja_der.append(distancia_ceja_der)
                    self.dist_ceja_izq.append(distancia_ceja_izq)
                    self.dist_nariz.append(distancia_nariz)
                    self.dist_forma.append(distancia_forma)
                    # Guardar y convertir la imagen recortada a formato base64
                    _, rostro_encoded = cv2.imencode('.png', imagen_color_con_landmarks)
                    rostro_base64 = base64.b64encode(rostro_encoded).decode('utf-8')
                    # Agregar rostros recortados a la lista
                    self.landmarks.append(rostro_base64)
            return self.landmarks, self.dist_ojo_der, self.dist_ojo_izq, self.dist_ceja_der, self.dist_ceja_izq, self.dist_nariz, self.dist_forma
        
        except Exception as e:
            # Manejo de errores
            print(f"Error en la detección de Landmarks: {e}")