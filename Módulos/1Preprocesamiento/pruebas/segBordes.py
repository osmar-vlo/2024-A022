import cv2

# Cargar la imagen y convertirla a escala de grises
img = cv2.imread('prueba.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Aplicar el detector de bordes Canny
umbral_min = 50
umbral_max = 150
edges = cv2.Canny(gray, umbral_min, umbral_max)
#Descarga
cv2.imwrite('segBordes.png', edges)