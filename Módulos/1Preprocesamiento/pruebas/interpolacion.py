import cv2

# Cargar la imagen
imagen = cv2.imread('prueba.jpg')

# Redimensionar la imagen con interpolación (interpolación Lanczos)
imagen_lan = cv2.resize(imagen, (600, 600), interpolation=cv2.INTER_LANCZOS4)

# Redimensionar la imagen con interpolación (interpolación Bicúbica)
imagen_bic = cv2.resize(imagen, (600, 600), interpolation=cv2.INTER_CUBIC)

# Descargar imagen
cv2.imwrite('imagen_lan.png', imagen_lan)
cv2.imwrite('imagen_bic.png', imagen_bic)