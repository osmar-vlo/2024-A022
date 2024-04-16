import cv2
import numpy as np

# Cargar la imagen y convertirla a escala de grises
img = cv2.imread('prueba.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar el detector de bordes Laplaciano
edges = cv2.Laplacian(gray, cv2.CV_64F)

# Convertir los bordes a una imagen binaria
edges = np.uint8(np.absolute(edges))
ret, edges_thresh = cv2.threshold(edges, 25, 255, cv2.THRESH_BINARY)

#Descarga
cv2.imwrite('segLaplaciano.png', edges_thresh)