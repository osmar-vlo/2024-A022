import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen en escala de grises
imagen = cv2.imread('prueba.jpg', cv2.IMREAD_GRAYSCALE)

# Calcular el histograma
histograma = cv2.calcHist([imagen], [0], None, [256], [0, 256])

# Normalizar el histograma (por ejemplo, ecualización del histograma)
imagen_ecualizada = cv2.equalizeHist(imagen)

# Mostrar la imagen original y la imagen ecualizada
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(imagen, cmap='gray')
plt.title('Imagen Original')

plt.subplot(1, 2, 2)
plt.imshow(imagen_ecualizada, cmap='gray')
plt.title('Imagen Ecualizada')

plt.show()