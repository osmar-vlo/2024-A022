import cv2

# Cargar el clasificador Haar para la detección de rostros y bocas
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_mcs_mouth.xml')

# Leer la imagen
img = cv2.imread('prueba.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detectar rostros en la imagen
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# Para cada rostro detectado, detectar la boca
for (x, y, w, h) in faces:
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]
    mouths = mouth_cascade.detectMultiScale(roi_gray)
    for i, (mx, my, mw, mh) in enumerate(mouths):
        mouth_roi = roi_color[my:my + mh, mx:mx + mw]
        cv2.imwrite(f'mouth_{i}.jpg', mouth_roi)

print('Bocas detectadas guardadas correctamente.')
