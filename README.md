# Análisis de Rentabilidad de Películas

Trabajo práctico para la **Carrera de Especialización en Inteligencia Artificial (CEIA)** — materia Aprendizaje de Máquinas.

El objetivo es predecir si una película será rentable (`revenue > budget`) antes de su estreno, usando únicamente información disponible en producción: presupuesto, duración, idioma, géneros, países y productoras.

**Integrantes:** Matías Guillermo Alfaro · Gonzalo Cuervo · Nicolas Alberto Tonnelier · Marina Andrea Racciatti

---

## Dataset

[Full TMDB Movies Dataset 2024](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies) (~1.4M películas).

Descargar `TMDB_movie_dataset_v11.csv` y colocarlo en `data/TMDB_movie_dataset_v11.csv` antes de ejecutar el notebook. El directorio `data/` no está commiteado.

## Setup

Requiere Python 3.12 y [`uv`](https://github.com/astral-sh/uv).

```bash
uv sync
uv run jupyter notebook
```

Abrir `prediction_movies_imdb.ipynb` y ejecutar las celdas en orden.

## Estructura del notebook

| Sección | Descripción |
|---|---|
| Setup y carga de datos | Importaciones y lectura del CSV |
| Descripción de los datos | Shape, tipos, estadísticas descriptivas |
| EDA | Distribuciones numéricas, variables categóricas, balance de clases, correlaciones y tasas de rentabilidad |
| Limpieza de datos | Eliminación de duplicados, películas para adultos y entradas con runtime/budget/revenue inválidos |
| Variable target | Creación de `profitable` (1 si `revenue > budget`) |
| Ingeniería de features | Encoding de variables categóricas, ensamblado de `X` e `y` |
| División train/test | Split 80/20 estratificado |
| Modelos | Regresión Logística, Random Forest, LightGBM, SVM |

## Features del modelo

- **Numéricas:** `budget`, `runtime`
- **Categóricas (encoded):** `original_language` (top 10 + other), `genres` (multi-hot), `production_countries` (top 20, multi-hot), `production_companies` (top 30, multi-hot)

`revenue` se excluye: no está disponible antes del estreno y define la variable target.
