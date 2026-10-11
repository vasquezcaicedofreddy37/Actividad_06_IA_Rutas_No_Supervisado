from dataclasses import dataclass
from heapq import heappush, heappop
from math import radians, sin, cos, sqrt, atan2
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class Estacion:
    nombre: str
    lat: float
    lon: float
    zona: str

ESTACIONES: Dict[str, Estacion] = {
    "Portal Norte": Estacion("Portal Norte", 4.7545, -74.0469, "Norte"),
    "Calle 100": Estacion("Calle 100", 4.6847, -74.0558, "Norte"),
    "Calle 72": Estacion("Calle 72", 4.6587, -74.0596, "Chapinero"),
    "Calle 45": Estacion("Calle 45", 4.6318, -74.0646, "Centro-Norte"),
    "Av. Jiménez": Estacion("Av. Jiménez", 4.6031, -74.0723, "Centro"),
    "Ricaurte": Estacion("Ricaurte", 4.6126, -74.0826, "Centro-Occidente"),
    "CAD": Estacion("CAD", 4.6233, -74.0890, "Occidente"),
    "Av. El Dorado": Estacion("Av. El Dorado", 4.6380, -74.0960, "Occidente"),
    "Portal El Dorado": Estacion("Portal El Dorado", 4.6908, -74.1295, "Occidente"),
    "Tercer Milenio": Estacion("Tercer Milenio", 4.5924, -74.0790, "Centro-Sur"),
    "NQS Calle 30 Sur": Estacion("NQS Calle 30 Sur", 4.5755, -74.1050, "Sur"),
    "Portal Sur": Estacion("Portal Sur", 4.5965, -74.1695, "Sur"),
}
CONEXIONES = {k: [] for k in ESTACIONES}

def conectar(a,b,costo,corredor):
    CONEXIONES[a].append((b,costo,corredor))
    CONEXIONES[b].append((a,costo,corredor))

for a,b,c,corr in [
    ("Portal Norte","Calle 100",8,"Autonorte"),
    ("Calle 100","Calle 72",4,"Autonorte"),
    ("Calle 72","Calle 45",4,"Caracas"),
    ("Calle 45","Av. Jiménez",5,"Caracas"),
    ("Av. Jiménez","Tercer Milenio",3,"Caracas"),
    ("Av. Jiménez","Ricaurte",4,"Eje Ambiental"),
    ("Ricaurte","CAD",3,"NQS"),
    ("CAD","Av. El Dorado",3,"NQS / El Dorado"),
    ("Av. El Dorado","Portal El Dorado",7,"El Dorado"),
    ("Ricaurte","NQS Calle 30 Sur",5,"NQS"),
    ("NQS Calle 30 Sur","Portal Sur",8,"NQS / Sur"),
    ("Calle 45","CAD",8.5,"Conexión académica"),
    ("Tercer Milenio","NQS Calle 30 Sur",6.5,"Conexión académica"),
]:
    conectar(a,b,c,corr)

def haversine(a,b):
    R=6371.0
    lat1,lon1,lat2,lon2=map(radians,[a.lat,a.lon,b.lat,b.lon])
    dlat,dlon=lat2-lat1,lon2-lon1
    h=sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2*R*atan2(sqrt(h),sqrt(1-h))

def buscar_ruta(origen,destino):
    if origen not in ESTACIONES or destino not in ESTACIONES:
        raise ValueError("Origen o destino no existe en la base de conocimiento.")

    frontera=[]
    heappush(frontera,(0.0,origen))
    costo={origen:0.0}
    previo={origen:None}
    exploracion=[]
    paso=0

    while frontera:
        f_actual, actual=heappop(frontera)
        paso+=1
        h_actual=haversine(ESTACIONES[actual],ESTACIONES[destino])
        exploracion.append({
            "paso": paso, "estacion": actual,
            "g": round(costo[actual],2), "h": round(h_actual,2),
            "f": round(costo[actual]+h_actual,2),
            "regla": "R4: comprobar si el estado actual es el destino."
        })

        if actual==destino:
            ruta=[]
            n=actual
            while n is not None:
                ruta.append(n); n=previo[n]
            ruta.reverse()
            detalles=[]
            for a,b in zip(ruta,ruta[1:]):
                vecino=next(x for x in CONEXIONES[a] if x[0]==b)
                detalles.append({"desde":a,"hasta":b,"costo":vecino[1],"corredor":vecino[2]})
            return {"ruta":ruta,"costo_total":round(costo[destino],2),
                    "detalles":detalles,"exploracion":exploracion}

        for vecino,costo_arista,corredor in CONEXIONES[actual]:
            nuevo=costo[actual]+costo_arista
            if vecino not in costo or nuevo<costo[vecino]:
                costo[vecino]=nuevo
                previo[vecino]=actual
                h=haversine(ESTACIONES[vecino],ESTACIONES[destino])
                heappush(frontera,(nuevo+h,vecino))

    raise ValueError("No se encontró una ruta.")
