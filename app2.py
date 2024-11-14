from flask import Flask, request, jsonify, render_template
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import math
from collections import defaultdict
import json
import time

app = Flask(__name__)

# Inicializar el stemmer y lista de stopwords
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Cargar índice invertido final
with open('final_inverted_index.json', 'r') as f:
    inverted_index = json.load(f)

# Cargar datos del CSV para consulta de detalles de los documentos
data_frame = pd.read_csv('data.csv')

# Función de procesamiento de consulta
def search_query(query, top_k):
    # Tokenización y preprocesamiento
    tokens = word_tokenize(query.lower())
    terms = [ps.stem(word) for word in tokens if word not in stop_words and word not in string.punctuation]
    
    # Lista de resultados (doc_id y tf-idf)
    results = []
    for term in terms:
        if term in inverted_index:
            for doc_id, data in inverted_index[term].items():
                tf_idf_score = data['tf-idf']
                results.append((doc_id, tf_idf_score))
    
    # Ordenar resultados por relevancia y limitar al top K
    results = sorted(results, key=lambda x: x[1], reverse=True)[:top_k]
    final_results = []
    for doc_id, relevance in results:
        # Acceder al contenido de cada documento desde el DataFrame
        row = data_frame.loc[data_frame['index'] == int(doc_id)].iloc[0]
        final_results.append({
            'doc_id': doc_id,
            'relevance': relevance,
            'title': row['title'],
            'genre': row['genre'],
            'summary': row['summary']
        })
    return final_results

@app.route('/')
def index():
    return render_template('index2.html')

# Endpoint de búsqueda
@app.route('/search', methods=['POST'])
def search():
    start_time = time.time()
    data = request.get_json()
    query = data.get('query')
    top_k = int(data.get('top_k', 5))

    # Ejecutar búsqueda en el índice invertido
    results = search_query(query, top_k)
    elapsed_time = time.time() - start_time

    return jsonify({
        'results': results,
        'elapsed_time': elapsed_time
    })

if __name__ == '__main__':
    app.run(debug=True)
