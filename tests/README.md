# Suite de Pruebas (API Testing)

Este directorio contiene los scripts para simular el tráfico transaccional hacia el microservicio y validar el comportamiento del motor XGBoost en producción.

## Justificación del Escenario de Pruebas

El script `test_api.py` inyecta dos transacciones simuladas basadas empíricamente en los resultados de explicabilidad (SHAP) obtenidos en la Etapa 3:

1. **Test de Control (Flujo Limpio):** Emula una transacción con variables latentes neutrales y un comportamiento de gasto alineado con el historial del usuario (`amount_diff_from_avg` mínimo). Esperado: Aprobación.
2. **Test de Anomalía (Fraude Simulado):** Emula un ataque transaccional alterando específicamente las variables que SHAP identificó como críticas:
   * **V14 y V4:** Se empujan hacia valores extremos (negativos y positivos, respectivamente) para gatillar los árboles de decisión principales.
   * **Contexto Temporal:** Se inyecta a las 3 AM (`hour_of_day`) con un monto que se desvía drásticamente de la media móvil de las últimas 50 transacciones (`amount_diff_from_avg` extremo), validando que las tuberías construidas en DuckDB impactan la inferencia final. Esperado: Bloqueo/Revisión Manual.
