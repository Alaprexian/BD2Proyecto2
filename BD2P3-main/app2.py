from flask import Flask, request, jsonify, send_file, render_template
import pickle
import numpy as np
import cv2
import os
from  metodos import KDTree, Sequential
app = Flask(__name__)

# Cargar el modelo K-Means y los histogramas preprocesados
with open("kmeans_model.pkl", "rb") as f:
    kmeans = pickle.load(f)
with open("histograms.pkl", "rb") as f:
    histograms_data = pickle.load(f)

histograms, labels, image_paths = histograms_data

kd_tree = KDTree(histograms)

# Función para calcular el histograma de una nueva imagen
def compute_histogram_for_image(image, kmeans):
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    if descriptors is not None:
        visual_words = kmeans.predict(descriptors)
        hist, _ = np.histogram(visual_words, bins=np.arange(kmeans.n_clusters + 1))
        return hist
    return None

# Endpoint para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para buscar similitudes
@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    # Leer imagen cargada
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

    if image is None:
        return jsonify({"error": "Invalid image"}), 400

    # Leer método de búsqueda seleccionado (por defecto: Sequential)
    method = request.form.get('method', 'Sequential')

    # Calcular histograma de la imagen de consulta
    query_hist = compute_histogram_for_image(image, kmeans)
    if query_hist is None:
        return jsonify({"error": "No descriptors found in the image"}), 400

    results = []

    if method == 'Sequential':
        # Búsqueda secuencial (cálculo directo de distancias)
        distances = [np.linalg.norm(query_hist - hist) for hist in histograms]
        top_indices = np.argsort(distances)[:5]
        for idx in top_indices:
            results.append({
                "label": labels[idx],
                "distance": round(distances[idx], 2),
                "path": image_paths[idx]
            })

    elif method == 'KDTree':
        # Búsqueda usando KD-Tree
        distances, indices = kd_tree.query(query_hist, k=5)
        for dist, idx in zip(distances, indices):
            results.append({
                "label": labels[idx],
                "distance": round(dist, 2),
                "path": image_paths[idx]
            })

    else:
        return jsonify({"error": "Invalid search method"}), 400

    return jsonify(results)

# Ruta para servir imágenes desde el servidor
@app.route('/image/<path:filename>', methods=['GET'])
def get_image(filename):
    return send_file(filename, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
