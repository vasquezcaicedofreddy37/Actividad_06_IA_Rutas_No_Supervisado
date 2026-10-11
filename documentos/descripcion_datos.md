# Descripción del conjunto de datos — Actividad 06

**Procedencia:** 600 recorridos sintéticos generados para la Actividad 05; no son observaciones reales ni datos oficiales de TransMilenio. Se reutilizan para asegurar continuidad académica.

**Variables de entrada de K-Means:** `distancia_km` (distancia simulada), `transbordos` (cantidad), `incidente` (0/1), `franja` (periodo del día) y `dia_tipo` (hábil/no hábil). Las categóricas se transforman a indicadores one-hot; todas las variables se estandarizan.

**Variables de contexto no usadas para agrupar:** `origen`, `destino`. **Variable excluida intencionalmente:** `congestion`, etiqueta de la actividad supervisada. Su uso para entrenar convertiría el ejercicio en un análisis dependiente de etiquetas.

**Salida:** `grupo_kmeans` es un identificador numérico arbitrario; no debe interpretarse automáticamente como congestión baja, media o alta. El número de grupos se elige comparando k de 2 a 6 con silhouette.

**Limitaciones:** datos sintéticos, posibles sesgos de simulación, sensibilidad a escalado, elección de variables y supuestos geométricos de K-Means. PCA es solo visualización.
