# Actividad 06 — Agrupamiento no supervisado de recorridos

Continuación del Sistema Inteligente de Rutas: frontend Flask + algoritmo A* + árbol de decisión de Actividad 05 + nuevo K-Means. **Datos sintéticos, no oficiales**.

## Instalación y ejecución
```powershell
pip install -r requirements.txt
python modelo_no_supervisado.py
python -m pytest pruebas/test_agrupamiento.py -v
python app.py
```
Visitar http://127.0.0.1:5000 para la aplicación de rutas. **K-Means se ejecuta por consola; no está integrado a la interfaz.**

## Resultados comprobados
- Registros: 600; k: 6; silhouette: 0.3984; Davies–Bouldin: 1.1751.
- Pruebas automatizadas: 4/4.

## Documentos
`documentos/descripcion_datos.md`, `documentos/pruebas_y_resultados.md`, `documentos/guion_video_10_min.md`; informe PDF en la raíz.

## Pendiente antes de entrega
Completar integrantes, URL real del repositorio, URL del video; publicar y agregar al tutor como colaborador. Cada integrante debe hacer sus propios commits; no fabricar historial Git.
