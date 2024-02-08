from flask import Flask, render_template, request
import cv2
import numpy as np
import base64
import json

app = Flask(__name__) # Crea una aplicación web Flask, y app se convierte en una instancia de esta aplicación.

app.static_folder = 'static'# Configurar la carpeta de archivos estáticos
app.static_url_path = '/static' # Configurar la ruta URL para archivos estáticos

@app.route('/') # Decorador para asociar una función (vista) con una ruta específica en tu aplicación web - Ruta Raiz
def index(): # Esta es la función asociada a la ruta '/'
    return render_template('index.html') # Busca un archivo llamado 'index.html' en el directorio de plantillas de tu aplicación.

@app.route('/preprocesamiento', methods=['POST'])
def procesar_imagen():
    try:
        # Leer la imagen en formato de matriz con OpenCV
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
        rostros_normalizados = []
        rostros_vectorizados = []
        rostros_recortados = []

        # Iterar sobre los rostros detectados
        for i, (x, y, w, h) in enumerate(rostros):
            # Dibujar rectángulos alrededor de los rostros detectados
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Recortar la región del rostro
            rostro_recortado = img[y:y+h, x:x+w]

            # Normalizar a nivel de píxel
            rostro_normalizado = rostro_recortado / 255.0  # Normalizar a [0, 1]

            # Vectorizar el rostro
            rostro_vectorizado = rostro_recortado.flatten()

            # Recortar la imagen del rostro a 50x50 píxeles
            rostro_recortado_pequeno = cv2.resize(rostro_recortado, (50, 50))

            # Convertir la imagen recortada a formato base64
            _, rostro_encoded = cv2.imencode('.png', rostro_recortado_pequeno)
            rostro_base64 = base64.b64encode(rostro_encoded).decode('utf-8')

            # Agregar rostros a las listas respectivas
            rostros_normalizados.append(rostro_normalizado.tolist())
            rostros_vectorizados.append(rostro_vectorizado.tolist())
            rostros_recortados.append({"imagen_base64": rostro_base64, "vectorizacion": rostro_vectorizado.tolist()})

        # Recortar la imagen principal a 300x300 píxeles
        img_recortada = cv2.resize(img, (250, 250))

        # Convertir la imagen recortada a formato base64
        _, img_recortada_encoded = cv2.imencode('.png', img_recortada)
        img_recortada_base64 = base64.b64encode(img_recortada_encoded).decode('utf-8')

        # Convertir la imagen de nuevo a formato base64 para mostrarla en HTML o para futuras acciones con el formato PNG
        _, img_encoded = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')

        # Guardar los datos en un archivo JSON
        datos_json = {
            "rostros_normalizados": rostros_normalizados,
            "rostros_vectorizados": rostros_vectorizados,
            "rostros_recortados": rostros_recortados
        }

        with open('datos_rostros.json', 'w') as json_file:
            json.dump(datos_json, json_file)

        # Renderizar la página con la imagen procesada y las imágenes recortadas de rostros
        return render_template('index.html', resultado=f"Imagen procesada con éxito. Rostros detectados: {len(rostros)}",
                       img_base64=img_base64, rostros_recortados=rostros_recortados,
                       img_recortada_base64=img_recortada_base64,
                       rostros_normalizados=rostros_normalizados,
                       rostros_vectorizados=rostros_vectorizados)
    except Exception as e:
        return render_template('index.html', resultado=f"Error al procesar la imagen: {str(e)}")
    
@app.route('/descargar_normalizacion')
def descargar_normalizacion():
    try:
        with open('datos_rostros.json', 'r') as json_file:
            datos = json.load(json_file)
        rostros_normalizados = datos.get('rostros_normalizados', [])
        return json.dumps(rostros_normalizados)
    except Exception as e:
        return str(e)

@app.route('/descargar_vectorizacion')
def descargar_vectorizacion():
    try:
        with open('datos_rostros.json', 'r') as json_file:
            datos = json.load(json_file)
        rostros_vectorizados = datos.get('rostros_vectorizados', [])
        return json.dumps(rostros_vectorizados)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'static/imagenes'
    app.run(debug=True)