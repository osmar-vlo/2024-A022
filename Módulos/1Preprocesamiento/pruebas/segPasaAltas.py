import cv2
import numpy as np

# Cargar la imagen y convertirla a escala de grises
img = cv2.imread('prueba.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar el filtro Pasa Altas
kernel_size = 3
kernel = np.array([[-1, -1, -1],
                   [-1,  8, -1],
                   [-1, -1, -1]])
high_pass = cv2.filter2D(gray, -1, kernel)

# Convertir los bordes a una imagen binaria
ret, edges_thresh = cv2.threshold(high_pass, 20, 255, cv2.THRESH_BINARY)

#Descarga
cv2.imwrite('segPasaAltas.png', edges_thresh)