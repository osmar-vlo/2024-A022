import cv2
import numpy as np

# Leer la imagen en escala de grises
img = cv2.imread('prueba.jpg')

# Convertir la imagen a formato de flotante y normalizar los valores de los píxeles
img_float = np.float32(img) / 255.0

# Aplicar el filtro Pasa Altas
kernel_size = 5  # Tamaño del kernel del filtro
kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size * kernel_size)  # Kernel de filtro promedio
highpass = img_float - cv2.filter2D(img_float, -1, kernel)  # Aplicar filtro Pasa Altas

# Convertir la imagen resultante de nuevo a formato de 8 bits sin signo
highpass = np.uint8(highpass * 255.0)

# Descarga
cv2.imwrite('pasaAltas2.png', highpass)