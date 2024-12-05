from flask import Flask, request, render_template, jsonify
import json
import time
from collections import Counter
import math
from Parte1 import preprocess_text
from collections import defaultdict
from Parte1 import normalize_vector
import pandas as pd



app = Flask(__name__)

# Cargar el índice invertido desde archivo

# Función para calcular el vector de consulta
def compute_query_vector(query, inverted_index, N):
    query_terms = preprocess_text(query)
    query_vector = {}
    term_counts = Counter(query_terms)
    
    for term, count in term_counts.items():
        if term in inverted_index:
            idf = math.log(N / len(inverted_index[term]))
            query_vector[term] = count * idf
    
    return query_vector

# Función para calcular la similitud de coseno
def cosine_similarity(query_vector, doc_vector):
    dot_product = sum(query_vector[term] * doc_vector.get(term, 0) for term in query_vector)
    query_norm = math.sqrt(sum(val ** 2 for val in query_vector.values()))
    doc_norm = math.sqrt(sum(val ** 2 for val in doc_vector.values()))
    if query_norm == 0 or doc_norm == 0:
        return 0
    return dot_product / (query_norm * doc_norm)

# Función de búsqueda
def search_similarity(query, num_results=10):
    query_terms = preprocess_text(query)
    
    # Cargar índice maestro
    with open('master_index.json', 'r') as f:
        master_index = json.load(f)

    # Identificar bloques relevantes
    relevant_blocks = set()
    for term in query_terms:
        if term in master_index:
            relevant_blocks.update(master_index[term])

    # Calcular el vector de la consulta
    query_vector = defaultdict(float)
    for term in query_terms:
        query_vector[term] += 1  # TF para la consulta

    query_vector = normalize_vector(query_vector)

    # Buscar en los bloques relevantes
    block_results = []
    for block_num in relevant_blocks:
        with open(f'block_{block_num}_normalized.json', 'r') as f:
            normalized_vectors = json.load(f)

        # Calcular similitud de coseno con cada documento en el bloque
        scores = {}
        for doc_id, doc_vector in normalized_vectors.items():
            similarity = cosine_similarity(query_vector, doc_vector)
            scores[doc_id] = similarity

        # Agregar los mejores resultados del bloque
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        block_results.extend(sorted_scores[:num_results])

    # Ordenar resultados finales y devolver los mejores
    block_results = sorted(block_results, key=lambda x: x[1], reverse=True)[:num_results]

    # Cargar el dataset original para obtener los summaries
    data = pd.read_csv('C:/Users/crist/go/BD2Proyecto2/data.csv')
    results_with_summary = []
    for doc_id, score in block_results:
        doc_id = int(doc_id) 
        if 0 <= doc_id < len(data):  # Verificamos que el índice sea válido
            row = data.iloc[doc_id]  # Obtenemos la fila correspondiente por posición
            summary = row['summary']
            title = row['title']
            genre = row['genre']
        else:
            summary = "Resumen no disponible"
            title = "Título no disponible"
            genre = "Género no disponible"
        results_with_summary.append({
            'doc_id': doc_id,
            'score': score,
            'title': title,
            'genre': genre,
            'summary': summary
        })
    
    return results_with_summary
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_route():
    query = request.form['query']
    top_k = int(request.form['top_k'])
    start_time = time.time()
    results = search_similarity(query, top_k)
    elapsed_time = time.time() - start_time
    return jsonify({
        'results': results,
        'elapsed_time': elapsed_time
    })


if __name__ == '__main__':
    app.run(debug=True)
