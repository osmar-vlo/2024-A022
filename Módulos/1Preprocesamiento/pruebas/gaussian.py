import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('prueba.jpg')

# Aplicar el filtro de suavizado gaussiano
blurred_img = cv2.GaussianBlur(img, (5, 5), 0)  # Tamaño del kernel: 5x5, desviación estándar: 0 (auto)

#Descarga
cv2.imwrite('gaussian.png', blurred_img)