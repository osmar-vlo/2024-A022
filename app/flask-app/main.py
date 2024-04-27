from Imagen import Imagen
from Rostro import Rostro

# Crear una instancia de la clase Imagen
imagen = Imagen('ressize.png')

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
