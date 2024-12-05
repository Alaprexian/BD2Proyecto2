import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import math
from collections import defaultdict
import json
import os

# Descargar datos de NLTK necesarios
#nltk.download('punkt')
#nltk.download('stopwords')

# Inicializar el stemmer y lista de stopwords
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Función de preprocesamiento
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    processed_tokens = [
        ps.stem(word) for word in tokens 
        if word not in stop_words and word not in string.punctuation
    ]
    return processed_tokens

# Función para construir el índice de un bloque
def build_block_inverted_index(data_block):
    block_inverted_index = defaultdict(dict)
    document_frequencies = defaultdict(int)

    for _, row in data_block.iterrows():
        doc_id = row['index']
        text = f"{row['title']} {row['genre']} {row['summary']}"
        terms = preprocess_text(text)

        # Calcular TF para cada término en el documento actual
        term_frequencies = defaultdict(int)
        for term in terms:                    
            term_frequencies[term] += 1

        # Añadir términos al índice invertido del bloque con su TF
        for term, tf in term_frequencies.items():
            block_inverted_index[term][doc_id] = tf
            document_frequencies[term] += 1

    # Calcular TF-IDF en el bloque
    N = len(data_block)
    for term, doc_list in block_inverted_index.items():
        idf = math.log(N / document_frequencies[term])
        for doc_id, tf in doc_list.items():
            block_inverted_index[term][doc_id] = tf * idf

    return block_inverted_index

# Función para guardar un bloque de índice en un archivo JSON
def save_block_to_disk(block_index, block_num):
    with open(f'block_{block_num}.json', 'w') as f:
        json.dump(block_index, f)
    print(f"Bloque {block_num} guardado en disco.")


# Función para normalizar vectores
def normalize_vector(vector):
    norm = math.sqrt(sum(val ** 2 for val in vector.values()))
    return {key: val / norm for key, val in vector.items()} if norm != 0 else vector

# Guardar bloque con vectores normalizados
def save_block_with_norms(block_index, block_num):
    normalized_index = {}
    for term, postings in block_index.items():
        for doc_id, tfidf in postings.items():
            if doc_id not in normalized_index:
                normalized_index[doc_id] = {}
            normalized_index[doc_id][term] = tfidf

    # Normalizar los vectores por documento
    normalized_vectors = {doc_id: normalize_vector(vector) for doc_id, vector in normalized_index.items()}
    
    # Guardar en disco
    with open(f'block_{block_num}_normalized.json', 'w') as f:
        json.dump(normalized_vectors, f)
    print(f"Bloque {block_num} normalizado guardado en disco.")

BLOCK_SIZE = 1000  # Número de documentos por bloque
data = pd.read_csv('C:/Users/crist/go/BD2Proyecto2/data.csv')
num_blocks = (len(data) + BLOCK_SIZE - 1) // BLOCK_SIZE

def build_blocks():
    # Crear el índice maestro mientras se procesan los bloques
    master_index = defaultdict(set)

    for block_num in range(num_blocks):
        start = block_num * BLOCK_SIZE
        end = min(start + BLOCK_SIZE, len(data))
        data_block = data.iloc[start:end]

        # Construir índice invertido del bloque
        block_index = build_block_inverted_index(data_block)
        save_block_to_disk(block_index, block_num)
        save_block_with_norms(block_index, block_num)

        # Actualizar índice maestro
        for term in block_index.keys():
            master_index[term].add(block_num)

    # Guardar el índice maestro
    with open('master_index.json', 'w') as f:
        json.dump({term: list(blocks) for term, blocks in master_index.items()}, f)
    print("Índice maestro guardado en disco.")

def cosine_similarity(query_vector, doc_vector):
    dot_product = sum(query_vector.get(term, 0) * doc_vector.get(term, 0) for term in query_vector)
    query_norm = math.sqrt(sum(val ** 2 for val in query_vector.values()))
    doc_norm = math.sqrt(sum(val ** 2 for val in doc_vector.values()))
    if query_norm == 0 or doc_norm == 0:
        return 0
    return dot_product / (query_norm * doc_norm)



# Parámetros de SPIMI
BLOCK_SIZE = 1000  # Número de documentos por bloque

"""
# Leer CSV
data = pd.read_csv('C:/Users/crist/go/BD2Proyecto2/data.csv')

num_blocks = (len(data) + BLOCK_SIZE - 1) // BLOCK_SIZE  # Calcular número de bloques necesarios

# Construcción de índice por bloques
for block_num in range(num_blocks):
    start = block_num * BLOCK_SIZE
    end = min(start + BLOCK_SIZE, len(data))
    data_block = data.iloc[start:end]

    # Construir y guardar el índice invertido del bloque
    block_index = build_block_inverted_index(data_block)
    save_block_to_disk(block_index, block_num)

# Combinar todos los bloques en un solo índice invertido final


build_blocks()

"""