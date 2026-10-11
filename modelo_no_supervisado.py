"""Actividad 06: K-Means para explorar patrones en recorridos sintéticos.
No utiliza la etiqueta congestion para entrenar. No son datos oficiales.
Ejecutar: python modelo_no_supervisado.py
"""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
COLUMNAS = ["distancia_km", "transbordos", "incidente"]
# Las variables categóricas se codifican con one-hot para evitar un orden artificial.
CATEGORICAS = ["franja", "dia_tipo"]

def cargar_datos(ruta=None):
    """Lee datos, verifica columnas y descarta registros incompletos."""
    ruta = Path(ruta) if ruta else BASE / "datos" / "recorridos_sinteticos.csv"
    df = pd.read_csv(ruta)
    requeridas = COLUMNAS + CATEGORICAS
    faltantes = set(requeridas) - set(df.columns)
    if faltantes:
        raise ValueError(f"Columnas faltantes: {sorted(faltantes)}")
    df = df.dropna(subset=requeridas).copy()
    if len(df) < 10:
        raise ValueError("Se necesitan al menos 10 registros completos")
    return df

def preparar_datos(df):
    """Convierte características a números y estandariza sus escalas."""
    # No se incluye congestion: es una etiqueta de la actividad supervisada.
    X = pd.get_dummies(df[COLUMNAS + CATEGORICAS], columns=CATEGORICAS, dtype=int)
    escalador = StandardScaler()
    return escalador.fit_transform(X), list(X.columns)

def seleccionar_k(X, minimo=2, maximo=6):
    """Compara números de grupos mediante el coeficiente silhouette."""
    evaluaciones = []
    for k in range(minimo, min(maximo, len(X)-1)+1):
        modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
        etiquetas = modelo.fit_predict(X)
        evaluaciones.append({"k": k,
            "silhouette": round(float(silhouette_score(X, etiquetas)), 4),
            "inercia": round(float(modelo.inertia_), 3)})
    elegido = max(evaluaciones, key=lambda x: x["silhouette"])["k"]
    return elegido, evaluaciones

def entrenar():
    """Entrena agrupamiento, exporta resultados, gráficos y métricas."""
    df = cargar_datos()
    X, columnas = preparar_datos(df)
    k, evaluaciones = seleccionar_k(X)
    modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
    grupos = modelo.fit_predict(X)
    resultado = df.copy()
    resultado["grupo_kmeans"] = grupos
    (BASE / "pruebas").mkdir(exist_ok=True)
    (BASE / "graficos").mkdir(exist_ok=True)
    resultado.to_csv(BASE / "datos" / "recorridos_agrupados.csv", index=False)
    perfil = resultado.groupby("grupo_kmeans").agg(
        cantidad=("grupo_kmeans", "size"), distancia_media_km=("distancia_km", "mean"),
        transbordos_medios=("transbordos", "mean"),
        porcentaje_incidentes=("incidente", "mean")).round(3)
    perfil["porcentaje_incidentes"] = (perfil["porcentaje_incidentes"]*100).round(1)
    perfil.to_csv(BASE / "pruebas" / "perfil_grupos.csv")
    metricas = {"total_registros": int(len(df)), "variables_modelo": columnas,
        "k_seleccionado": int(k), "comparacion_k": evaluaciones,
        "silhouette_final": round(float(silhouette_score(X, grupos)),4),
        "davies_bouldin": round(float(davies_bouldin_score(X, grupos)),4),
        "tamanos_grupos": {str(a):int(b) for a,b in resultado.grupo_kmeans.value_counts().sort_index().items()},
        "nota": "Agrupaciones exploratorias de datos sintéticos; no equivalen a categorías reales de congestión."}
    (BASE / "pruebas" / "metricas_agrupamiento.json").write_text(json.dumps(metricas, indent=2, ensure_ascii=False), encoding="utf-8")
    # PCA se utiliza exclusivamente para visualizar, no para entrenar K-Means.
    xy = PCA(n_components=2).fit_transform(X)
    plt.figure(figsize=(8,5))
    plt.scatter(xy[:,0],xy[:,1],c=grupos,cmap="viridis",s=17,alpha=.75)
    plt.title("Agrupamiento K-Means (proyección PCA) — datos sintéticos")
    plt.xlabel("Componente principal 1");plt.ylabel("Componente principal 2")
    plt.tight_layout();plt.savefig(BASE / "graficos" / "clusters_pca.png",dpi=160);plt.close()
    plt.figure(figsize=(7,4))
    plt.plot([e["k"] for e in evaluaciones],[e["silhouette"] for e in evaluaciones],marker="o")
    plt.title("Selección de k mediante silhouette")
    plt.xlabel("Número de grupos (k)");plt.ylabel("Silhouette")
    plt.tight_layout();plt.savefig(BASE / "graficos" / "seleccion_k.png",dpi=160);plt.close()
    print(json.dumps(metricas, indent=2, ensure_ascii=False))
    print("\nPerfiles de grupos:\n",perfil.to_string())
    return resultado, metricas

if __name__ == "__main__":
    entrenar()
