import cv2
import numpy as np
import matplotlib.pyplot as plt

# Leer la imagen en escala de grises
img = cv2.imread('prueba.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar el filtro de Sobel en la dirección X (horizontal)
sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)  # ksize es el tamaño del kernel (debe ser impar)

# Aplicar el filtro de Sobel en la dirección Y (vertical)
sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

# Calcular la magnitud del gradiente
sobel_mag = np.sqrt(sobel_x**2 + sobel_y**2)

# Mostrar la imagen original y la magnitud del gradiente resultante
plt.subplot(1, 3, 1), plt.imshow(img, cmap='gray'), plt.title('Original')
plt.subplot(1, 3, 2), plt.imshow(sobel_x, cmap='gray'), plt.title('Sobel X')
plt.subplot(1, 3, 3), plt.imshow(sobel_mag, cmap='gray'), plt.title('Magnitud del Gradiente')
plt.show()
