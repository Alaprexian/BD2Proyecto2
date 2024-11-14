# Proyecto: SPIMI Data Query

## Descripción General
DataFusionDB es un proyecto enfocado en la integración de diferentes modelos de datos y técnicas avanzadas de recuperación de información en una base de datos. El proyecto incluye la implementación de un índice invertido para búsqueda de texto completo y una interfaz web para interactuar con el índice.

## Objetivos
- Desarrollar un índice invertido para realizar búsquedas eficientes en colecciones de texto.
- Implementar la funcionalidad de SPIMI para manejar grandes colecciones de datos en memoria secundaria.
- Crear un frontend interactivo donde los usuarios puedan ingresar consultas textuales, especificar el número de resultados (Top K) y elegir el método de indexación.

## Funcionalidades Implementadas

### Backend
- **Preprocesamiento de Texto**: Se utiliza `nltk` para la tokenización, eliminación de stopwords y stemming.
- **Índice Invertido con TF-IDF**: Implementación de un índice invertido que utiliza TF-IDF para calcular la relevancia de términos en los documentos.
- **SPIMI (Single-Pass In-Memory Indexing)**: Para manejar grandes volúmenes de datos, se dividió el índice en bloques que se almacenan en memoria secundaria, los cuales luego se combinan en un índice final.
- **Almacenamiento en JSON**: El índice invertido se guarda en formato JSON para evitar recalculaciones innecesarias y mejorar la eficiencia en la carga.

### Frontend
- **Aplicación Web con Flask**: Se utilizó Flask para crear un servidor web que permite realizar consultas en el índice invertido.
- **Interfaz de Usuario**: Se creó una interfaz en HTML y CSS donde el usuario puede:
  - Ingresar una consulta textual.
  - Especificar el número de documentos a recuperar (Top K).
  - Ver los resultados de la búsqueda con el tiempo de ejecución de cada consulta.
- **Consulta y Recuperación de Resultados**: La aplicación busca en el índice invertido utilizando similitud de coseno y devuelve los documentos más relevantes.

## Estructura de Archivos

- `app.py`: Archivo principal de la aplicación web, que contiene las rutas de Flask y la lógica para realizar consultas.
- `Parte1.py`: Contiene la implementación del índice invertido y el algoritmo SPIMI para el almacenamiento de grandes volúmenes de datos.
- `templates/index.html`: Interfaz de usuario que permite realizar consultas de búsqueda.
- `data.csv`: Archivo CSV de datos original que contiene los documentos a indexar.
- `data_duplicated.csv`: Archivo duplicado de `data.csv` para pruebas con un conjunto de datos más grande.
- `final_inverted_index.json`: Índice invertido almacenado en memoria secundaria en formato JSON.

## Ejecución

1. **Requisitos**: 
   ```bash
   pip install pandas nltk flask


2. ## Preparar el Índice:
- Ejecuta `Parte1.py` para construir y guardar el índice invertido en `final_inverted_index.json`.

3. ## Iniciar la Aplicación:
- Inicia el servidor Flask desde app.py con el comando:
```bash
   python app.py
```
- Ingresa a la dirección creada para acceder a la interfaz de busqueda.

