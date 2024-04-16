import cv2

# Cargar el clasificador Haar para la detección de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Leer la imagen
img = cv2.imread('prueba.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detectar rostros en la imagen
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# Para cada rostro detectado, recortar la región de la frente
for (x, y, w, h) in faces:
    forehead_roi = img[y:y + int(h / 4), x:x + w]
    cv2.imwrite('forehead.jpg', forehead_roi)

print('Región de la frente recortada y guardada correctamente como "forehead.jpg".')