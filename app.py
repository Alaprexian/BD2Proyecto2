from flask import Flask, request, render_template, jsonify
import json
import time
from collections import Counter
import math
from Parte1 import preprocess_text

app = Flask(__name__)

# Cargar el índice invertido desde archivo
with open('final_inverted_index.json', 'r') as f:
    inverted_index = json.load(f)

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
def search(query, inverted_index, top_k=5):
    N = len(inverted_index)  # Número total de documentos
    query_vector = compute_query_vector(query, inverted_index, N)
    scores = []
    for doc_id in {doc for term in query_vector for doc in inverted_index.get(term, {})}:
        doc_vector = {term: inverted_index[term][doc_id] for term in query_vector if doc_id in inverted_index[term]}
        score = cosine_similarity(query_vector, doc_vector)
        scores.append((doc_id, score))
    ranked_results = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
    return ranked_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_route():
    query = request.form['query']
    top_k = int(request.form['top_k'])
    start_time = time.time()
    results = search(query, inverted_index, top_k)
    elapsed_time = time.time() - start_time
    return jsonify({
        'results': results,
        'elapsed_time': elapsed_time
    })

if __name__ == '__main__':
    app.run(debug=True)
