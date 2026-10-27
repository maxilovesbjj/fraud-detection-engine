# Fraud Risk Engine - BPO Optimization

Motor de detección de fraudes transaccionales diseñado para optimizar operaciones BPO (Business Process Outsourcing). 
El objetivo principal de esta arquitectura es reducir el AHT (Average Handling Time) del analista y minimizar la carga operativa generada por falsos positivos mediante machine learning y reglas de negocio.

## Etapas del Proyecto (En desarrollo)

1. **Métricas y Modelado Base:** Manejo de datos desbalanceados con SMOTE. Evaluación estricta enfocada en Precision, Recall y Matriz de Confusión (descartando Accuracy).
2. **Feature Engineering y Reglas:** Creación de variables temporales y despliegue de un motor de reglas duras previo a la evaluación del modelo.
3. **Explicabilidad Matemática (SHAP):** Generación de *Feature Importance* para justificar las alertas de alto riesgo ante los operadores humanos.
4. **Despliegue y Arquitectura:** Serialización del modelo con Joblib, exposición mediante endpoints en FastAPI y consumo en un dashboard web para el equipo de revisión.

## Stack Tecnológico
- **Core ML:** Python 3.11, Scikit-Learn, Imbalanced-Learn, XGBoost, SHAP.
- **Backend & Infraestructura:** FastAPI, Docker.
- **Frontend Operativo:** React, Tailwind CSS.