"""Actividad 05: aprendizaje supervisado sobre el proyecto académico de rutas.

El conjunto de datos es SINTÉTICO. No corresponde a registros reales de TransMilenio.
Se usa un árbol de decisión para predecir el nivel de congestión estimado
(baja, media o alta) a partir de características observables del recorrido.
"""
from pathlib import Path
import json
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

BASE = Path(__file__).resolve().parent
DATA = BASE / "datos" / "recorridos_sinteticos.csv"
OUT = BASE / "pruebas"
OUT.mkdir(exist_ok=True)


def entrenar():
    # 1. Cargar el dataset y comprobar las variables esperadas.
    datos = pd.read_csv(DATA)
    variables = ["origen", "destino", "franja", "dia_tipo", "distancia_km", "transbordos", "incidente"]
    objetivo = "congestion"
    assert set(variables + [objetivo]).issubset(datos.columns), "Faltan columnas"
    X, y = datos[variables], datos[objetivo]
    # 2. Separar 25 % de los registros para una evaluación independiente.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    categoricas = ["origen", "destino", "franja", "dia_tipo"]
    numericas = ["distancia_km", "transbordos", "incidente"]
    # 3. Codificar texto solo con el entrenamiento, evitando fuga de información.
    procesador = ColumnTransformer([
        ("categoricas", OneHotEncoder(handle_unknown="ignore"), categoricas),
        ("numericas", "passthrough", numericas),
    ])
    # 4. Entrenar el clasificador con límites para reducir el sobreajuste.
    modelo = Pipeline([
        ("preparacion", procesador),
        ("arbol", DecisionTreeClassifier(max_depth=5, min_samples_leaf=8, random_state=42)),
    ])
    modelo.fit(X_train, y_train)
    # 5. Evaluar sin reutilizar registros del conjunto de prueba en entrenamiento.
    pred = modelo.predict(X_test)
    metricas = {
        "registros": len(datos), "entrenamiento": len(X_train), "prueba": len(X_test),
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "validacion_cruzada_accuracy_media": round(float(cross_val_score(modelo, X, y, cv=5, scoring="accuracy").mean()), 4),
        "matriz_confusion_etiquetas": list(modelo.classes_),
        "matriz_confusion": confusion_matrix(y_test, pred, labels=modelo.classes_).tolist(),
        "reporte_clasificacion": classification_report(y_test, pred, output_dict=True, zero_division=0),
        "advertencia": "Datos sintéticos con etiquetas definidas por reglas académicas; no validan desempeño real."
    }
    # 6. Guardar modelo y resultados para su reproducción y revisión.
    joblib.dump(modelo, BASE / "modelo_congestion.joblib")
    (OUT / "metricas.json").write_text(json.dumps(metricas, ensure_ascii=False, indent=2), encoding="utf-8")
    nombres = modelo.named_steps["preparacion"].get_feature_names_out()
    (OUT / "reglas_arbol.txt").write_text(export_text(modelo.named_steps["arbol"], feature_names=list(nombres)), encoding="utf-8")
    print(json.dumps({k:v for k,v in metricas.items() if k != "reporte_clasificacion"}, ensure_ascii=False, indent=2))
    return modelo


def predecir_ejemplo(modelo):
    # 7. Simular un nuevo caso con el mismo esquema del dataset.
    caso = pd.DataFrame([{
        "origen": "Portal Norte", "destino": "Portal El Dorado",
        "franja": "pico_manana", "dia_tipo": "habil",
        "distancia_km": 17.5, "transbordos": 2, "incidente": 1
    }])
    resultado = str(modelo.predict(caso)[0])
    print("Predicción académica para nuevo caso:", resultado)
    return resultado


if __name__ == "__main__":
    predecir_ejemplo(entrenar())
