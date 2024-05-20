import json
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

from Imagen import Imagen
from Rostro import Rostro

# Definir el diccionario de rutas por etnia
etnia_rutas = {
    "Hispanos": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Hispano/datos.json",
    "Afrodescendientes": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Afro/datos.json",
    "Arabes": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Árabes/datos.json",
    "Asia": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Asia/datos.json",
    "Europa": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Europa/datos.json"
}

# Cargar y combinar los datos de todas las etnias
data_combined = []
for etnia, json_file_path in etnia_rutas.items():
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        data_combined.extend(data)

# Extraer características de los datos combinados
X = []

for instance in data_combined:
    # Verificar que todas las claves están presentes en el vector
    vector = instance.get("vector", {})
    required_keys = ["distancia_36_33", "distancia_39_33", "distancia_42_33", "distancia_45_33", "distancia_48_33", "distancia_54_33"]
    if all(key in vector for key in required_keys):
        # Usar las distancias como características
        distancia_36_33 = vector["distancia_36_33"][0]
        distancia_39_33 = vector["distancia_39_33"][0]
        distancia_42_33 = vector["distancia_42_33"][0]
        distancia_45_33 = vector["distancia_45_33"][0]
        distancia_48_33 = vector["distancia_48_33"][0]
        distancia_54_33 = vector["distancia_54_33"][0]

        X.append([distancia_36_33, distancia_39_33, distancia_42_33, distancia_45_33, distancia_48_33, distancia_54_33])
    else:
        print(f"Instancia ignorada por falta de claves: {instance}")

# Convertir a array de NumPy
X = np.array(X)

# Leer imagen y procesar características
path_user = '/home/mxn/Documents/2024-A022/DatasetAgeGif/Europa/woman/g2ugPGK/frame_1.png'
imagen = Imagen(path_user)
imagen_lan, imagen_gris = imagen.preprocesamiento()
gris_rois, color_rois = imagen.deteccion_facial(imagen_lan, imagen_gris)
rostro = Rostro(gris_rois, color_rois)
img, landmarks, distancia_36_33, distancia_39_33, distancia_42_33, distancia_45_33, distancia_48_33, distancia_54_33 = rostro.get_landmarks_vector()

# Crear un array con las distancias de la imagen procesada
Y = np.array([distancia_36_33, distancia_39_33, distancia_42_33, distancia_45_33, distancia_48_33, distancia_54_33]).reshape(1, -1)

# Calcular la distancia euclidiana entre la imagen procesada y cada instancia del dataset combinado
distancias_euclidianas = euclidean_distances(Y, X)

# Ordenar las distancias euclidianas de menor a mayor
indices_ordenados = np.argsort(distancias_euclidianas, axis=1)
distancias_ordenadas = distancias_euclidianas[np.arange(indices_ordenados.shape[0])[:, None], indices_ordenados]

# Obtener el índice del vecino más cercano (con la menor distancia euclidiana)
indice_menor_distancia = indices_ordenados[0][0]

# Obtener la ruta de la imagen correspondiente al vecino más cercano
ruta_imagen_menor_distancia = data_combined[indice_menor_distancia]["ruta_imagen"]

print("Distancias euclidianas ordenadas de menor a mayor:")
print(distancias_ordenadas)
print("Ruta de la imagen con la menor distancia euclidiana:")
print(ruta_imagen_menor_distancia)