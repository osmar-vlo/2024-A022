import cv2
import numpy as np

imagen = cv2.imread('prueba.jpg')#Cargar la imagen

imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)#Escala de grises 

media = np.mean(imagen_gris)#Calcular la media 
desviacion = np.std(imagen_gris)#Desviación estándar de la imagen

imagen_normalizada = (imagen_gris - media) / desviacion #Aplicar la normalización a la imagen

imagen_normalizada = np.clip(imagen_normalizada * 255, 0, 255).astype(np.uint8)

cv2.imwrite('imagen_normalizada.jpg', imagen_normalizada)#Descargar imagen 