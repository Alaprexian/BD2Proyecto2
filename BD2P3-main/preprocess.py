import os
import cv2
import random
import numpy as np
from sklearn.cluster import KMeans
import pickle

def load_images(base_path, sample_size=None):
    """
    Carga imágenes desde subcarpetas.

    Args:
        base_path (str): Ruta base donde están las subcarpetas.
        sample_size (int, optional): Número de imágenes por clase a cargar.

    Returns:
        dict: Diccionario con clases como claves y listas de imágenes como valores.
        dict: Diccionario con clases como claves y rutas de las imágenes como valores.
    """
    images = {}
    image_paths = {}
    for label in os.listdir(base_path):
        class_path = os.path.join(base_path, label)
        if os.path.isdir(class_path):
            files = [os.path.join(class_path, f) for f in os.listdir(class_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if sample_size:
                files = random.sample(files, min(sample_size, len(files)))
            image_paths[label] = files
            images[label] = [cv2.imread(f, cv2.IMREAD_GRAYSCALE) for f in files]
    return images, image_paths

def extract_descriptors(images):
    """
    Extrae descriptores locales usando SIFT.

    Args:
        images (dict): Diccionario con clases como claves y listas de imágenes como valores.

    Returns:
        dict: Diccionario con clases como claves y listas de descriptores como valores.
    """
    sift = cv2.SIFT_create()
    descriptors = {}
    for label, img_list in images.items():
        descriptors[label] = []
        for img in img_list:
            if img is not None:
                keypoints, desc = sift.detectAndCompute(img, None)
                if desc is not None:
                    descriptors[label].append(desc.astype(np.float32))  # Conversión a float32
    return descriptors

def flatten_descriptors(descriptors):
    """
    Convierte el diccionario de descriptores en una lista plana.

    Args:
        descriptors (dict): Diccionario con descriptores por clase.

    Returns:
        np.ndarray: Lista plana de todos los descriptores.
    """
    all_descriptors = []
    for desc_list in descriptors.values():
        for desc in desc_list:
            all_descriptors.extend(desc)
    return np.array(all_descriptors)

def compute_histograms_with_paths(descriptors, kmeans, image_paths):
    """
    Calcula histogramas de palabras visuales para cada imagen.

    Args:
        descriptors (dict): Diccionario de descriptores por clase.
        kmeans (KMeans): Modelo KMeans entrenado.
        image_paths (dict): Diccionario con rutas de imágenes.

    Returns:
        list: Histogramas de palabras visuales.
        list: Etiquetas de imágenes.
        list: Rutas de imágenes.
    """
    histograms = []
    labels = []
    paths = []
    for label, desc_list in descriptors.items():
        for i, desc in enumerate(desc_list):
            visual_words = kmeans.predict(desc)
            hist, _ = np.histogram(visual_words, bins=np.arange(kmeans.n_clusters + 1))
            histograms.append(hist)
            labels.append(label)
            paths.append(image_paths[label][i])
    return histograms, labels, paths

# Ruta base
BASE_IMAGE_PATH = "C:/Users/Hans/Downloads/expresiones/test"

# Carga imágenes y rutas
images, image_paths = load_images(BASE_IMAGE_PATH, sample_size=50)
print("Imágenes cargadas.")

# Extrae descriptores
descriptors = extract_descriptors(images)
print("Descriptores extraídos.")

# Aplana descriptores para KMeans
all_descriptors = flatten_descriptors(descriptors)
print(f"Descriptores totales: {all_descriptors.shape}")

# Entrena el modelo KMeans
NUM_CLUSTERS = 50
kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42)
kmeans.fit(all_descriptors)
print("Modelo K-Means entrenado.")

# Calcula histogramas
histograms, labels, paths = compute_histograms_with_paths(descriptors, kmeans, image_paths)
print("Histogramas calculados.")

# Guarda los datos procesados
with open("kmeans_model.pkl", "wb") as f:
    pickle.dump(kmeans, f)
with open("histograms.pkl", "wb") as f:
    pickle.dump((histograms, labels, paths), f)

print("Preprocesamiento completado. Datos guardados.")
