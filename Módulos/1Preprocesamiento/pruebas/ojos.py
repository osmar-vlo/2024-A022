import cv2

# Cargar el clasificador Haar para la detección de rostros y ojos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Leer la imagen
img = cv2.imread('prueba.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detectar rostros en la imagen
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# Para cada rostro detectado, detectar los ojos
for (x, y, w, h) in faces:
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for i, (ex, ey, ew, eh) in enumerate(eyes):
        eye_roi = roi_color[ey:ey + eh, ex:ex + ew]
        cv2.imwrite(f'eye_{i}.jpg', eye_roi)

print('Ojos detectados guardados correctamente.')
