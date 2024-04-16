import cv2

# Cargar la imagen
imagen = cv2.imread('prueba.jpg')

# Redimensionar la imagen a 300x300 píxeles, 1:1
imagen_300px = cv2.resize(imagen, (300, 300))

# Redimensionar la imagen a 300x300 píxeles, 4:3
imagen_400px = cv2.resize(imagen, (400, 300))

# Redimensionar la imagen a 600x600 píxeles, Max
imagen_600px = cv2.resize(imagen, (600, 600))

# Descargar imagen 300px
cv2.imwrite('imagen_300px.png', imagen_300px) 

# Descargar imagen 400px
cv2.imwrite('imagen_400px.png', imagen_400px) 

# Descargar imagen 600px
cv2.imwrite('imagen_600px.png', imagen_600px)