import cv2
# Leer la imagen
img = cv2.imread('prueba.jpg')

# Aplicar el filtro de mediana
median_filtered = cv2.medianBlur(img, 5)  # El segundo parámetro es el tamaño del kernel (debe ser impar)

# Descarga
cv2.imwrite('mediana.png', median_filtered)