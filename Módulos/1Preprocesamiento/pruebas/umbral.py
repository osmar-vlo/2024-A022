import cv2
import numpy as np

# Cargar la imagen y convertirla a escala de grises
img = cv2.imread('prueba.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar la umbralización
umbral = 127  # Umbral de intensidad
max_val = 255  # Valor máximo asignado a píxeles superiores al umbral
tipo_umbral = cv2.THRESH_BINARY  # Tipo de umbralización
ret, thresh = cv2.threshold(gray, umbral, max_val, tipo_umbral)

#Descarga
cv2.imwrite('umbral.png', thresh)