from flask import Flask, render_template, jsonify, request
from main import ESTACIONES, CONEXIONES, buscar_ruta

app = Flask(__name__)

@app.get("/")
def inicio():
    return render_template("index.html")

@app.get("/api/estaciones")
def estaciones():
    return jsonify([
        {"nombre": e.nombre, "zona": e.zona, "lat": e.lat, "lon": e.lon}
        for e in ESTACIONES.values()
    ])

@app.get("/api/conocimiento")
def conocimiento():
    conexiones=[]
    vistos=set()
    for origen, vecinos in CONEXIONES.items():
        for destino,costo,corredor in vecinos:
            llave=tuple(sorted([origen,destino]))
            if llave not in vistos:
                vistos.add(llave)
                conexiones.append({"origen":origen,"destino":destino,
                                   "costo":costo,"corredor":corredor})
    return jsonify({"estaciones":len(ESTACIONES),"conexiones":conexiones})

@app.post("/api/ruta")
def ruta():
    data=request.get_json(silent=True) or {}
    try:
        resultado=buscar_ruta(data.get("origen",""),data.get("destino",""))
        return jsonify(resultado)
    except ValueError as e:
        return jsonify({"error":str(e)}),400

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
