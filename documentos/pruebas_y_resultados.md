# Evidencias de ejecución y pruebas

Comandos ejecutados:

```powershell
python modelo_no_supervisado.py
python -m pytest pruebas/test_agrupamiento.py -v
```

- Registros: **600**.
- Grupos seleccionados por silhouette: **6**.
- Silhouette final: **0.3984** (mayor suele indicar mejor separación relativa).
- Davies–Bouldin: **1.1751** (menor suele indicar mejor compactación/separación).
- Tamaños: **{'0': 129, '1': 107, '2': 125, '3': 110, '4': 38, '5': 91}**.
- Pruebas automatizadas: **4 aprobadas**.

Se guardaron las salidas de consola en `pruebas/salida_entrenamiento.txt` y `pruebas/salida_pytest.txt`. El perfil descriptivo de cada grupo está en `pruebas/perfil_grupos.csv`.

**Interpretación:** son segmentos exploratorios, no clases predefinidas ni indicadores oficiales de congestión.
