from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import json
from models.JSON import JSON

app = Flask(__name__)
CORS(app) # Habilita CORS para toda la aplicación

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preprocesamiento', methods=['POST'])
def procesar_imagen():
    try:
        img_bytes = request.files['imagen'].read()
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Cargar el clasificador de Haar para la detección de rostros
        cascada_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Convertir la imagen a escala de grises
        imagen_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en la imagen
        rostros = cascada_rostros.detectMultiScale(imagen_gris, scaleFactor=1.3, minNeighbors=5)

        # Listas para almacenar rostros normalizados, vectorizados y recortados
        rostros_recortados = []

        # Iterar sobre los rostros detectados
        for i, (x, y, w, h) in enumerate(rostros):
            # Recortar la región del rostro
            rostro_recortado = img[y:y+h, x:x+w]

            # Recortar la imagen del rostro a 50x50 píxeles
            rostro_recortado_pequeno = cv2.resize(rostro_recortado, (300, 300))

            # Convertir la imagen recortada a formato base64
            _, rostro_encoded = cv2.imencode('.png', rostro_recortado_pequeno)
            rostro_base64 = base64.b64encode(rostro_encoded).decode('utf-8')

            # Agregar rostros recortados a la lista
            rostros_recortados.append({"imagen_base64": rostro_base64})

        # Formar la respuesta
        response_data = {
            "resultado": f"Imagen procesada con éxito. Rostros detectados: {len(rostros)}",
            "rostros_recortados": rostros_recortados
        }

        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)