import os
import json
import cv2
import base64
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from Imagen import Imagen
from Rostro import Rostro

# Función para procesar una imagen
def procesar_imagen(ruta_imagen, subcarpeta, subcarpeta_interna):
    try:
        # Crear una instancia de la clase Imagen para la imagen actual
        imagen = Imagen(ruta_imagen)
        
        # Realizar el preprocesamiento y obtener las imágenes procesadas
        imagen_lan, imagen_gris = imagen.preprocesamiento()
        
        # Realizar la detección facial y obtener los ROIs
        gris_rois, color_rois = imagen.deteccion_facial(imagen_lan, imagen_gris)
        
        # Crear una instancia de la clase Rostro con los ROIs obtenidos
        rostro = Rostro(gris_rois, color_rois)
        
        # Llamar al método get_landmarks_vector para procesar los ROIs y obtener landmarks
        img, landmarks, vector, distancia_36_33, distancia_39_33, distancia_42_33, distancia_45_33, distancia_48_33, distancia_54_33, dist_ojo_der, dist_ojo_izq, dist_ceja_der, dist_ceja_izq, dist_nariz, dist_forma = rostro.get_landmarks_vector()
        # Obtener la etiqueta de la imagen basada en el nombre del archivo y la estructura de carpetas
        nombre_archivo = os.path.splitext(os.path.basename(ruta_imagen))[0]  # Obtener el nombre del archivo sin la extensión
        edad = int(nombre_archivo.split('_')[-1])  # Extraer la edad del nombre del archivo
        # Calcular la edad basada en el nombre del archivo y ajustarla a las etiquetas deseadas
        if edad == 0:
            edad_base = 10
        else:
            edad_base = (edad + 1) * 10

        genero = os.path.basename(subcarpeta)
        etiqueta = f"{genero}_{edad_base}"  # Formar la etiqueta combinando género y edad
        
        ruta = subcarpeta +"/"+ subcarpeta_interna # Formar ruta para descargar image

        # Guardar las imágenes en archivos PNG
        for i, img_data in enumerate(img):
            img_bytes = base64.b64decode(img_data)
            img_np = np.frombuffer(img_bytes, dtype=np.uint8)
            imge = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
            ruta_nueva_img = os.path.join(ruta+"/Results", f"img_{etiqueta}.png")
            cv2.imwrite(ruta_nueva_img, imge)

        for i, land_data in enumerate(landmarks):
            land_bytes = base64.b64decode(land_data)
            land_np = np.frombuffer(land_bytes, dtype=np.uint8)
            land = cv2.imdecode(land_np, cv2.IMREAD_COLOR)
            ruta_nueva_land = os.path.join(ruta+"/Results", f"land_{etiqueta}.png")
            cv2.imwrite(ruta_nueva_land, land)

        # Crear un diccionario con los datos de interés para esta imagen
        response_data = {
            "ruta_imagen": ruta_imagen,
            "ruta_nueva_imagen": ruta_nueva_img,
            "ruta_nuevo_landmark": ruta_nueva_land,
            "etiqueta": etiqueta,
            "vector": vector,
            "distancia_36_33": distancia_36_33,
            "distancia_39_33": distancia_39_33,
            "distancia_42_33": distancia_42_33,
            "distancia_45_33": distancia_45_33,
            "distancia_48_33": distancia_48_33,
            "distancia_54_33": distancia_54_33,
            "dist_ojo_der": dist_ojo_der,
            "dist_ojo_izq": dist_ojo_izq,
            "dist_ceja_der": dist_ceja_der,
            "dist_ceja_izq": dist_ceja_izq,
            "dist_nariz": dist_nariz,
            "dist_forma": dist_forma
        }

        return response_data
    
    except Exception as e:
        # Manejo de errores
        print(f"Error al procesar imagen (main): {e}")

# Función para procesar todas las imágenes de una carpeta
def procesar_carpeta(ruta_carpeta):
    try: 
        subcarpeta, subcarpeta_interna = os.path.split(ruta_carpeta)
        print(f"Proceso {os.getpid()} está procesando la carpeta {subcarpeta}/{subcarpeta_interna}")

        response_data_list = []

        # Obtener la lista de archivos PNG en la carpeta
        archivos_png = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.png')]
        
        with ThreadPoolExecutor() as executor:
            # Ejecutar múltiples hilos para procesar cada imagen en paralelo
            futures = [executor.submit(procesar_imagen, os.path.join(ruta_carpeta, archivo), subcarpeta, subcarpeta_interna) for archivo in archivos_png]
            # Obtener los resultados de los hilos a medida que se completan
            for future in as_completed(futures):
                response_data_list.append(future.result())

        return response_data_list
    except Exception as e:
        # Manejo de errores
        print(f"Error al leer carpeta (main): {e}")

# Ruta base donde se encuentran las subcarpetas "man" y "woman"
carpeta_base = '/home/mxn/Documents/2024-A022/app/flask-app/pruebas'
subcarpetas = ['man', 'woman']  # Nombre de las subcarpetas que contienen las imágenes

response_data_list = []  # Definir la lista de respuesta fuera del contexto del executor

# Iterar sobre las subcarpetas para procesar cada carpeta en paralelo
for subcarpeta in subcarpetas:
    ruta_subcarpeta = os.path.join(carpeta_base, subcarpeta)
    subcarpetas_internas = [nombre for nombre in os.listdir(ruta_subcarpeta) if os.path.isdir(os.path.join(ruta_subcarpeta, nombre))]
    
    for subcarpeta_interna in subcarpetas_internas:
        ruta_subcarpeta_interna = os.path.join(ruta_subcarpeta, subcarpeta_interna)
        
        # Ejecutar la función para procesar todas las imágenes de la carpeta en paralelo
        ruta_resultados = os.path.join(ruta_subcarpeta_interna, "Results")
        os.makedirs(ruta_resultados, exist_ok=True)

        response_data_list.extend(procesar_carpeta(ruta_subcarpeta_interna))

# Guardar la lista de datos de respuesta en un solo archivo JSON
json_file_path = os.path.join(carpeta_base, 'datos.json')

with open(json_file_path, 'w') as json_file:
    json.dump(response_data_list, json_file, indent=4)

print(f"Datos guardados en JSON correctamente en {json_file_path}.")