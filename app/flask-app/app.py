from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64

app = Flask(__name__)
CORS(app) # Habilita CORS para toda la aplicación

@app.route('/')
def index():
    return render_template('index.html')

from Imagen import Imagen
from Rostro import Rostro

@app.route('/preprocesamiento', methods=['POST'])
def procesar_imagen():
    try:
        img_bytes = request.files['imagen'].read()
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Crear una instancia de la clase Imagen
        imagen = Imagen(npimg)

        # Realizar el preprocesamiento y obtener las imágenes procesadas
        imagen_lan, imagen_gris = imagen.preprocesamiento()

        # Realizar la detección facial y obtener los ROIs
        gris_rois, color_rois = imagen.deteccion_facial(imagen_lan, imagen_gris)

        # Crear una instancia de la clase Rostro con los ROIs obtenidos
        rostro = Rostro(gris_rois, color_rois)

        # Llamar al método get_landmarks_image para procesar los ROIs y obtener landmarks
        landmarks, dist_ojo_der, dist_ojo_izq, dist_ceja_der, dist_ceja_izq, dist_nariz, dist_forma = rostro.get_landmarks_image()

        response_data_list = []
        for i in range(len(landmarks)):
            response_data = {
                "landmarks": landmarks[i],
                "dist_ojo_der": dist_ojo_der[i],
                "dist_ojo_izq": dist_ojo_izq[i],
                "dist_ceja_der": dist_ceja_der[i],
                "dist_ceja_izq": dist_ceja_izq[i],
                "dist_nariz": dist_nariz[i],
                "dist_forma": dist_forma[i]
            }
            response_data_list.append(response_data)

        for data in response_data_list:
            print(data)

        # Listas para almacenar rostros normalizados, vectorizados y recortados
        rostros_recortados = []

        # Agregar rostros recortados a la lista
        rostros_recortados.append({"imagen_base64": landmarks})

        # Formar la respuesta
        response_data = {
            "resultado": f"Imagen procesada con éxito. Rostros detectados: {len(landmarks)}",
            "rostros_recortados": rostros_recortados
        }

        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)