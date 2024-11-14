# Proyecto 2 & 3: Búsqueda y Recuperación de la Información - DataFusionDB

## Descripción General
**DataFusionDB** es una aplicación que integra diferentes modelos de datos y técnicas avanzadas de recuperación de información para una base de datos de tipo multimedia, que incluye documentos de texto y otros tipos de datos. Este proyecto implementa:
1. Un índice invertido para búsquedas de texto completo (Parte 1).
2. Un sistema de almacenamiento para grandes colecciones usando SPIMI.
3. Una interfaz web para realizar consultas y visualizar resultados.

## Objetivos
1. Construir un índice invertido que soporte consultas de texto en lenguaje natural.
2. Implementar el algoritmo SPIMI para manejo de grandes volúmenes de datos en memoria secundaria.
3. Desarrollar una interfaz de usuario para realizar búsquedas sobre los datos indexados y presentar resultados.

## Estructura del Proyecto
- `Parte1.py`: Implementación de SPIMI para construir el índice invertido en bloques.
- `app.py`: Backend de Flask que maneja las solicitudes de búsqueda.
- `templates/index.html`: Interfaz de usuario para realizar consultas y ver los resultados.
- `data.csv`: Archivo original de datos con columnas `index`, `title`, `genre`, y `summary`.
- `final_inverted_index.json`: Archivo JSON que almacena el índice invertido final después de construirlo con SPIMI.

## Funcionalidades Implementadas
## Backend
- `Preprocesamiento de Texto`: Se utiliza nltk para la tokenización, eliminación de stopwords y stemming.
- `Índice Invertido con TF-IDF`: Implementación de un índice invertido que utiliza TF-IDF para calcular la relevancia de términos en los documentos.
- `SPIMI (Single-Pass In-Memory Indexing)`: Para manejar grandes volúmenes de datos, se dividió el índice en bloques que se almacenan en memoria secundaria, los cuales luego se combinan en un índice final.
- `Almacenamiento en JSON`: El índice invertido se guarda en formato JSON para evitar recalculaciones innecesarias y mejorar la eficiencia en la carga.

## Instalación y Ejecución
### Requisitos
- Python 3.x
- Paquetes: Flask, pandas, nltk

### Instalación de Dependencias
```bash
pip install flask pandas nltk
