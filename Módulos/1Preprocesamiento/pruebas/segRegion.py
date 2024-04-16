import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('prueba.jpg')

# Convertir la imagen a formato RGB (OpenCV carga imágenes en formato BGR)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Redimensionar la imagen para facilitar el procesamiento
resized_img = cv2.resize(img_rgb, (img.shape[1] // 4, img.shape[0] // 4))

# Convertir la imagen redimensionada a un formato adecuado para k-means
reshaped_img = resized_img.reshape((-1, 3)).astype(np.float32)  # Convertir a float32

# Definir el número de clusters para k-means (número de regiones deseadas)
num_clusters = 5

# Aplicar k-means para segmentar la imagen en regiones
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
_, labels, centers = cv2.kmeans(reshaped_img, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Asignar a cada píxel el color del centroide al que pertenece
segmented_img = centers[labels.flatten()].reshape(resized_img.shape).astype(np.uint8)

#Descarga
cv2.imwrite('segRegion.png', segmented_img)