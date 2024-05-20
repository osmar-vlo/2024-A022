import json
import numpy as np
import cv2
import os
import base64
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split

from Imagen import Imagen
from Rostro import Rostro
from GIFGenerator import GIFGenerator

etiqueta = "woman_30"
etnia = "Europa"

# Definir el diccionario de rutas por etnia
etnia_rutas = {
    "Hispanos": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Dataset/datos.json",
    "Afrodescendientes": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Afrodescendientes/datos.json",
    "Asia": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Asia/datos.json",
    "Europa": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Europa/datos.json"
}

# Seleccionar la ruta del archivo JSON según la etnia
json_file_path = etnia_rutas.get(etnia, None)

if json_file_path is None:
    raise ValueError(f"No se encontró la ruta para la etnia: {etnia}")

# Cargar los datos desde el archivo JSON
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Filtrar las instancias que tengan la etiqueta específica
filtered_data = [instance for instance in data if instance["etiqueta"] == etiqueta]

# Extraer características de los datos filtrados
X = []

for instance in filtered_data:
    # Usar las distancias como características
    distancia_36_33 = instance["distancia_36_33"][0]
    distancia_39_33 = instance["distancia_39_33"][0]
    distancia_42_33 = instance["distancia_42_33"][0]
    distancia_45_33 = instance["distancia_45_33"][0]
    distancia_48_33 = instance["distancia_48_33"][0]
    distancia_54_33 = instance["distancia_54_33"][0]

    X.append([distancia_36_33, distancia_39_33, distancia_42_33, distancia_45_33, distancia_48_33, distancia_54_33])

# Convertir a array de NumPy
X = np.array(X)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test = train_test_split(X, test_size=0.3, random_state=42)

# Verificar la forma de X_train
print(X_train.shape)

# Crear el modelo KNN para búsqueda de imágenes similares
knn_model = NearestNeighbors(n_neighbors=5)
knn_model.fit(X_train)

def find_similar_images(reference_image_features):
    # Verificar que reference_image_features tenga al menos una característica
    if len(reference_image_features) == 0 or any(len(feature) == 0 for feature in reference_image_features):
        raise ValueError("reference_image_features está vacío o contiene arrays vacíos")

    # Convertir las características de referencia a un array numpy
    reference_image_features_array = np.array(reference_image_features).reshape(1, -1)

    # Encontrar imágenes similares usando KNN
    distances, indices = knn_model.kneighbors(reference_image_features_array)

    # Obtener índices de imágenes similares
    indices_flat = indices.flatten()

    return indices_flat

# Leer imagen y procesar características
path_joven = '/home/mxn/Documents/2024-A022/Images de Prueba/rt.jpg'
imagen = Imagen(path_joven)
imagen_lan, imagen_gris = imagen.preprocesamiento()
gris_rois, color_rois = imagen.deteccion_facial(imagen_lan, imagen_gris)
rostro = Rostro(gris_rois, color_rois)
img, landmarks, vector, distancia_36_33, distancia_39_33, distancia_42_33, distancia_45_33, distancia_48_33, distancia_54_33, dist_ojo_der, dist_ojo_izq, dist_ceja_der, dist_ceja_izq, dist_nariz, dist_forma = rostro.get_landmarks_vector()

# Guardar las imágenes en archivos PNG
for i, img_data in enumerate(img):
    img_bytes = base64.b64decode(img_data)
    img_np = np.frombuffer(img_bytes, dtype=np.uint8)
    img_recortada = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

# Ejemplo de uso para encontrar imágenes similares a una imagen de referencia
reference_image_features = [distancia_36_33, distancia_39_33, distancia_42_33, distancia_45_33, distancia_48_33, distancia_54_33]

# Verificar que reference_image_features tenga datos válidos
print("Número de características en reference_image_features:", len(reference_image_features))

similar_image_indices = find_similar_images(reference_image_features)

# Obtener rutas de imágenes similares usando los índices encontrados
similar_image_paths = [filtered_data[index]['ruta_nueva_imagen'] for index in similar_image_indices]
print(similar_image_paths)

# Generar un GIF por cada ruta encontrada
output_folder = '/home/mxn/Documents/2024-A022/app/flask-app/pruebas/'

# En tu loop para generar los GIFs, donde creas una instancia de GIFGenerator
for i, path in enumerate(similar_image_paths):
    # Leer la imagen y obtener su representación base64
    with open(path, "rb") as img_file:
        img_data = img_file.read()
        img_base64 = base64.b64encode(img_data).decode()

    # Usar img_base64 en lugar de img en GIFGenerator
    gif_generator = GIFGenerator(
        img_recortada,  # Usar la representación base64 de la imagen
        img_base64,
        os.path.join(output_folder, f'imagen_intermedia_{i}.gif')
    )
    gif_generator.generate_gif()