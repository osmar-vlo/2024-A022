from flask import Flask, render_template, request
import cv2
import numpy as np
import base64
import json

app = Flask(__name__)

app.static_folder = 'static'
app.static_url_path = '/static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preprocesamiento', methods=['POST'])
def procesar_imagen():
    try:
        img_bytes = request.files['imagen'].read()
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        cascada_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        imagen_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        rostros = cascada_rostros.detectMultiScale(imagen_gris, scaleFactor=1.3, minNeighbors=5)

        rostros_recortados = []

        for i, (x, y, w, h) in enumerate(rostros):
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            rostro_recortado = img[y:y+h, x:x+w]
            rostro_recortado_pequeno = cv2.resize(rostro_recortado, (500, 500))
            _, rostro_encoded = cv2.imencode('.png', rostro_recortado_pequeno)
            rostro_base64 = base64.b64encode(rostro_encoded).decode('utf-8')
            rostros_recortados.append({"imagen_base64": rostro_base64})

        img_recortada = cv2.resize(img, (250, 250))
        _, img_recortada_encoded = cv2.imencode('.png', img_recortada)
        img_recortada_base64 = base64.b64encode(img_recortada_encoded).decode('utf-8')

        _, img_encoded = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')

        datos_json = {
            "rostros_recortados": rostros_recortados
        }

        with open('datos_rostros.json', 'w') as json_file:
            json.dump(datos_json, json_file)

        return render_template('index.html', resultado=f"Imagen procesada con éxito. Rostros detectados: {len(rostros)}",
                       img_base64=img_base64, rostros_recortados=rostros_recortados,
                       img_recortada_base64=img_recortada_base64)
    except Exception as e:
        return render_template('index.html', resultado=f"Error al procesar la imagen: {str(e)}")
    
if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'static/imagenes'
    app.run(debug=True)