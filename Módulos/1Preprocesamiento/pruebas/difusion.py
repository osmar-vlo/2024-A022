import cv2
import matplotlib.pyplot as plt

# Leer la imagen
img = cv2.imread('prueba.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar la difusión anisotrópica
diffused_img = cv2.ximgproc.anisotropicDiffusion(img, alpha=0.1, K=50, iterations=10)

#Descarga
cv2.imwrite('difusion.png', diffused_img)