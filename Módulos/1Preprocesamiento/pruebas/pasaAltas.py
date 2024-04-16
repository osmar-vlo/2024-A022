import cv2
import numpy as np

# Leer la imagen en escala de grises
img = cv2.imread('prueba.jpg')

# Aplicar el filtro Pasa Altas
kernel_size = 3  # Tamaño del kernel del filtro
high_pass = cv2.filter2D(img, -1, np.array([[-1, -1, -1],
                                            [-1,  8, -1],
                                            [-1, -1, -1]]))

# Descarga
cv2.imwrite('pasaAltas.png', high_pass)