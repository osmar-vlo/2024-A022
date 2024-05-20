import json
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

from Imagen import Imagen
from Rostro import Rostro

path_user = '/home/mxn/Documents/2024-A022/DatasetAgeGif/Europa/woman/g2ugPGK/frame_1.png'
etnia = "Europa"
etiqueta = "woman"

# Definir el diccionario de rutas por etnia
etnia_rutas = {
    "Hispanos": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Hispano/datos.json",
    "Afrodescendientes": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Afro/datos.json",
    "Arabes": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Árabes/datos.json",
    "Asia": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Asia/datos.json",
    "Europa": "/home/mxn/Documents/2024-A022/DatasetAgeGif/Europa/datos.json"
}

# Cargar los datos solo de la etnia específica
json_file_path = etnia_rutas[etnia]
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)
    print(f"Cargados {len(data)} registros de {etnia}")

# Filtrar las instancias que tengan la etiqueta específica
filtered_data = [instance for instance in data if instance["etiqueta"] == etiqueta]

# Extraer características y rutas de los datos filtrados
X = []
rutas = []
etiquetas = []

for instance in data:
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
        rutas.append(instance["ruta_imagen"])
        etiquetas.append(instance["etiqueta"])
    else:
        print(f"Instancia ignorada por falta de claves: {instance}")

# Convertir a array de NumPy
X = np.array(X)
rutas = np.array(rutas)
etiquetas = np.array(etiquetas)

# Verificar la forma de los datos
print(f"Forma de X: {X.shape}")

# Definir los índices de prueba basados en las etiquetas
test_labels = ["man_30", "man_50", "man_70", "woman_30", "woman_50", "woman_70"]
test_indices = np.isin(etiquetas, test_labels)
train_indices = ~test_indices

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test = X[train_indices], X[test_indices]
rutas_train, rutas_test = rutas[train_indices], rutas[test_indices]

# Verificar las divisiones
print(f"Total de instancias: {len(data)}")
print(f"Instancias de entrenamiento: {len(X_train)}")
print(f"Instancias de prueba: {len(X_test)}")

if len(X_train) == 0 or len(X_test) == 0:
    raise ValueError("Uno de los conjuntos de datos (entrenamiento o prueba) está vacío.")

# Implementar KNN para encontrar los 5 vecinos más cercanos en el conjunto de entrenamiento
def encontrar_vecinos_mas_cercanos(Y, X_train, rutas_train, k=5):
    distancias_euclidianas = euclidean_distances(Y, X_train)
    indices_menores_distancias = np.argsort(distancias_euclidianas.ravel())[:k]
    return rutas_train[indices_menores_distancias]

# Leer imagen y procesar características de la imagen de prueba
imagen = Imagen(path_user)
imagen_lan, imagen_gris = imagen.preprocesamiento()
gris_rois, color_rois = imagen.deteccion_facial(imagen_lan, imagen_gris)
rostro = Rostro(gris_rois, color_rois)
img, landmarks, distancia_36_33, distancia_39_33, distancia_42_33, distancia_45_33, distancia_48_33, distancia_54_33 = rostro.get_landmarks_vector()

# Crear un array con las distancias de la imagen procesada
Y = np.array([distancia_36_33, distancia_39_33, distancia_42_33, distancia_45_33, distancia_48_33, distancia_54_33]).reshape(1, -1)

# Encontrar las rutas de las 5 imágenes más cercanas en el conjunto de entrenamiento
rutas_imagenes_menores_distancias_train = encontrar_vecinos_mas_cercanos(Y, X_train, rutas_train, k=5)

print("Rutas de las 5 imágenes más cercanas en el conjunto de entrenamiento:")
print(rutas_imagenes_menores_distancias_train)