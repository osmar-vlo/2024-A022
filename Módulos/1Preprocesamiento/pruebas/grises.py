import cv2

# Lee la imagen en color
imagen_color = cv2.imread('prueba.jpg')

# Convierte la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2GRAY)

# Guarda la imagen en escala de grises
cv2.imwrite('grises.jpg', imagen_gris)
