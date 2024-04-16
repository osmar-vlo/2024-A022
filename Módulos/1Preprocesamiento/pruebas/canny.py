import cv2
import numpy as np

# Cargar la imagen en escala de grises
img = cv2.imread('prueba.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar el filtro de Canny
edges = cv2.Canny(img, 100, 200)  # Puedes ajustar los valores de umbral según sea necesario

#Descarga
cv2.imwrite('canny.png', edges)