# Transactional Fraud Detection Engine

Motor de detección de fraudes transaccionales diseñado bajo una arquitectura de microservicios para operaciones BPO (Business Process Outsourcing) en el sector financiero. 

Este proyecto implementa un sistema predictivo de extremo a extremo (End-to-End), priorizando el procesamiento de alto rendimiento, el manejo matemático del desbalance de clases y la explicabilidad de las decisiones.

---

## Alcance del Proyecto

En entornos de monitoreo transaccional, el costo operativo de revisar falsos positivos es crítico. El objetivo de este motor es maximizar la tasa de captura de fraudes reales (Recall) manteniendo una alta pureza en las alertas generadas (Precision), garantizando además que cada alerta incluya un desglose de las variables que gatillaron la decisión para facilitar la auditoría humana.

---

## Arquitectura y Proceso (Data Pipelines)

El flujo de datos está diseñado lógicamente como un sistema de tuberías, minimizando cuellos de botella desde la ingesta hasta la inferencia en producción:

1. **Succión y Procesamiento Analítico (DuckDB):** Procesamiento de datos crudos utilizando un motor OLAP en memoria. Se emplean *Window Functions* en SQL para calcular variables de comportamiento temporal (ej. medias móviles de gasto de las últimas 50 transacciones) en milisegundos.
2. **Cámara de Modelado (XGBoost):** Entrenamiento del modelo predictivo utilizando árboles de decisión con gradient boosting. En lugar de inyectar datos sintéticos (SMOTE), el desbalance extremo de clases se maneja mediante el parámetro nativo `scale_pos_weight`.
3. **Módulo de Explicabilidad (SHAP):** Implementación de valores SHAP (Shapley Additive exPlanations) para abrir la "caja negra" del modelo y cuantificar el impacto de cada variable en tiempo real.
4. **Válvula de Salida y Despliegue (FastAPI + Docker):** Serialización del motor con `joblib` y exposición a través de una API REST contenerizada, capaz de recibir cargas JSON y devolver veredictos de fraude en milisegundos.

---

## Pruebas de Estrés (Testing)

El repositorio incluye una suite de pruebas en el directorio `/tests` para validar el comportamiento del microservicio en producción. Los tests simulan la inyección de transacciones limpias y ataques anómalos, alterando específicamente las variables de mayor peso predictivo descubiertas en el análisis SHAP (V14 y V4) y forzando desviaciones en el caudal de gasto histórico.

---

## Resultados Técnicos

La calibración de los pesos matemáticos (`scale_pos_weight` = 577.29) sobre el motor XGBoost arrojó las siguientes métricas sobre el conjunto de validación:

* **Recall (85%):** El modelo captura exitosamente a 85 de cada 100 transacciones fraudulentas.
* **Precisión (89%):** De cada 100 alertas derivadas a los analistas, 89 son fraudes reales confirmados.
* **Exactitud Global (99.9% sobre 56.962 transacciones):** Métrica no representativa dado el desbalance extremo; la calibración operativa se centró en maximizar Recall y Precisión.

---

## Conclusiones Operativas

1. **Eficiencia Técnica sobre Datos Sintéticos:** La penalización matemática nativa de XGBoost demostró ser superior a técnicas de sobremuestreo como SMOTE. Al evitar la distorsión del espacio de datos, se logró contener la caída de la Precisión, un factor vital para no saturar los centros de operaciones BPO con revisiones innecesarias.
2. **Validación del Feature Engineering:** El análisis SHAP confirmó que las variables de comportamiento temporal creadas mediante DuckDB (`rolling_avg_amount_50` y `amount_diff_from_avg`) se posicionaron con un alto peso predictivo, demostrando que el análisis del contexto transaccional es más robusto que la evaluación de transacciones aisladas.
3. **Madurez para Producción:** La contenerización del microservicio garantiza que el motor puede integrarse de manera agnóstica a cualquier infraestructura en la nube o sistema *legacy* bancario.

---

## Stack Tecnológico

* **Data Engineering:** DuckDB, Pandas, Parquet.
* **Machine Learning:** XGBoost, Scikit-Learn, SHAP, Joblib.
* **Backend & DevOps:** Python 3.10, FastAPI, Uvicorn, Docker.
