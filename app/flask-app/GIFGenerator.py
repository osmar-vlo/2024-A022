import cv2
import base64
import numpy as np
import imageio

class GIFGenerator:
    def __init__(self,img_joven, img_mayor_base64, output_folder):

        self.img_joven = img_joven

        img_bytes = base64.b64decode(img_mayor_base64)
        img_np = np.frombuffer(img_bytes, dtype=np.uint8)
        self.img_mayor = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        # Guardar la ruta del archivo de salida
        self.output_path = output_folder

        self.num_frames = 100
        self.duration = 100

    def generate_gif(self):
        imagenes_intermedias = []
        for i in range(self.num_frames - 10):
            factor_mezcla = i / (self.num_frames + 1)  # Factor de mezcla entre 0 y 1
            img_intermedia = cv2.addWeighted(self.img_joven, 1 - factor_mezcla, self.img_mayor, factor_mezcla, 0)
            imagenes_intermedias.append(img_intermedia)

        imagenes_intermedias_rgb = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in imagenes_intermedias]

        imageio.mimsave(self.output_path, imagenes_intermedias_rgb, duration=self.duration)

        print(f'GIF animado generado: {self.output_path}')