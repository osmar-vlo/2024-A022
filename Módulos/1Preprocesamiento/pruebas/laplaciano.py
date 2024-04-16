import cv2
import numpy as np

# Lee la imagen en escala de grises
img = cv2.imread('prueba.jpg', cv2.IMREAD_GRAYSCALE)

# Aplica el filtro Laplaciano
laplacian = cv2.Laplacian(img, cv2.CV_64F)

# Convierte la imagen resultante a un formato adecuado para visualización
laplacian = np.uint8(np.absolute(laplacian))

# Descarga
cv2.imwrite('laplaciano.png', laplacian)