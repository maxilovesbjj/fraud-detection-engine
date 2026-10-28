# Fraud Detection Engine (BPO)

Repositorio principal de un motor de detección de fraudes transaccionales, diseñado bajo una arquitectura de microservicios orientada a operaciones BPO (Business Process Outsourcing) en el sector financiero.

## Arquitectura de Datos
- \data/raw/\: Datos crudos inmutables.
- \data/processed/\: Datos limpios y estandarizados.
- \data/features/\: Variables de comportamiento (Feature Engineering).

## Etapas del Proyecto (Roadmap)

### Etapa 1: Fundamentos y Métricas (Completada)
- Análisis base de desbalance de clases.
- Evaluación empírica de SMOTE vs Random Forest base.
- Traducción de métricas (Precision/Recall) a impacto operativo BPO.

### Etapa 2: Ingeniería de Características y Reglas (Completada)
- Generación de variables temporales y de comportamiento.
- Procesamiento de alto rendimiento con DuckDB y Pandas.
- Diseño de reglas duras de negocio.

### Etapa 3: Modelado Avanzado y Explicabilidad (Completada)
- Entrenamiento con XGBoost.
- Calibración de umbrales de decisión.
- Explicabilidad de inferencias usando SHAP.

### Etapa 4: Despliegue en Producción (Completada)
- Serialización del motor con Joblib.
- Creación de microservicio API con FastAPI.
- Contenerización con Docker (Dockerfile listo para despliegue).
