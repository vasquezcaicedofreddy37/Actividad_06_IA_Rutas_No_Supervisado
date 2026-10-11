"""Pruebas automáticas del modelo no supervisado."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from modelo_no_supervisado import cargar_datos, preparar_datos, seleccionar_k, entrenar

def test_dataset_valido():
    datos=cargar_datos()
    assert len(datos)==600
    assert datos[["distancia_km","transbordos","incidente"]].notna().all().all()

def test_preparacion_sin_etiquetas():
    datos=cargar_datos()
    X, columnas=preparar_datos(datos)
    assert len(X)==len(datos)
    assert "congestion" not in columnas
    assert X.shape[1]==len(columnas)

def test_seleccion_k_reproducible():
    X,_=preparar_datos(cargar_datos())
    k, evaluaciones=seleccionar_k(X)
    assert 2<=k<=6
    assert len(evaluaciones)==5

def test_exportaciones():
    df, m=entrenar()
    assert df.grupo_kmeans.nunique()==m["k_seleccionado"]
    assert (Path(__file__).resolve().parents[1]/"graficos/clusters_pca.png").exists()
