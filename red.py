import numpy as np
from PIL import Image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet import preprocess_input, decode_predictions

# Cargar el modelo preentrenado de ResNet50
model = ResNet50(weights='imagenet')

# Función para cargar y preprocesar una imagen
def preprocess_image(image_path):
    # Cargar la imagen
    image = Image.open(image_path)
    # Redimensionar la imagen a 224x224 píxeles
    image_resized = image.resize((224, 224))
    # Convertir la imagen a un array numpy
    image_array = np.array(image_resized)
    # Asegurar que la imagen esté en el rango [0, 255] y sea de tipo float32
    image_array = image_array.astype(np.float32) / 255.0
    # Agregar una dimensión adicional para la muestra
    image_array = np.expand_dims(image_array, axis=0)
    # Preprocesar la imagen de acuerdo con las especificaciones de ResNet50
    preprocessed_image = preprocess_input(image_array)
    return preprocessed_image

# Función para predecir la edad a partir de una imagen
def predict_age(image_path):
    preprocessed_image = preprocess_image(image_path)
    preds = model.predict(preprocessed_image)
    # Aquí puedes procesar las predicciones según tus necesidades
    return preds

# Ejemplo de uso
image_path = '/home/mxn/Documents/2024-A022/app/static/img/rt.jpg'  # Ruta de tu imagen
predictions = predict_age(image_path)
print(predictions)
