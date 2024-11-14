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

# Función para cargar bloques y combinarlos en un índice invertido final
def merge_blocks(num_blocks):
    final_inverted_index = defaultdict(dict)

    for block_num in range(num_blocks):
        with open(f'block_{block_num}.json', 'r') as f:
            block_index = json.load(f)

            # Combinar términos de cada bloque en el índice final
            for term, postings in block_index.items():
                if term not in final_inverted_index:
                    final_inverted_index[term] = postings
                else:
                    final_inverted_index[term].update(postings)

    # Guardar el índice combinado en un archivo JSON
    with open('final_inverted_index.json', 'w') as f:
        json.dump(final_inverted_index, f)
    print("Índice invertido final guardado en disco.")

# Parámetros de SPIMI
BLOCK_SIZE = 1000  # Número de documentos por bloque

"""
# Leer CSV
data = pd.read_csv('data.csv')
for i in range(5):
    data = pd.concat([data, data], ignore_index=True)
num_blocks = (len(data) + BLOCK_SIZE - 1) // BLOCK_SIZE  # Calcular número de bloques necesarios

# Construcción de índice por bloques
#
for block_num in range(num_blocks):
    start = block_num * BLOCK_SIZE
    end = min(start + BLOCK_SIZE, len(data))
    data_block = data.iloc[start:end]

    # Construir y guardar el índice invertido del bloque
    block_index = build_block_inverted_index(data_block)
    save_block_to_disk(block_index, block_num)

# Combinar todos los bloques en un solo índice invertido final
merge_blocks(num_blocks)
"""