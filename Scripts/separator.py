import os
from PIL import Image
from datetime import datetime

# Obtener la ruta de la carpeta con los archivos GIF
folder_path = '/home/mxn/Documents/2024-A022/DatasetAgeGif/Asia/man'

# Obtener la lista de archivos GIF en la carpeta
gif_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.gif')]

# Procesar cada archivo GIF por separado
for gif_file in gif_files:
    # Crear una carpeta con el nombre del archivo GIF (sin extensión)
    gif_name = os.path.splitext(gif_file)[0]
    output_folder = os.path.join(folder_path, gif_name)
    os.makedirs(output_folder, exist_ok=True)

    # Abrir el archivo GIF
    gif_path = os.path.join(folder_path, gif_file)
    gif_imagen = Image.open(gif_path)

    # Extraer y guardar cada frame del GIF
    frames = []
    try:
        while True:
            gif_imagen.seek(gif_imagen.tell() + 1)
            frames.append(gif_imagen.copy())
    except EOFError:
        pass

    # Guardar cada frame como imagen individual dentro de la carpeta
    for i, frame in enumerate(frames):
        frame.save(os.path.join(output_folder, f'frame_{i}.png'))  # Cambiar la extensión si deseas

    # Mover el archivo GIF analizado a la carpeta
    analyzed_gif_path = os.path.join(output_folder, gif_file)
    os.rename(gif_path, analyzed_gif_path)

print("Archivos GIF procesados y movidos a carpetas individuales.")