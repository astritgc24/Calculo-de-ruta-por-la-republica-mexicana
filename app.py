from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Coordenadas de las ciudades
coord = {
    'Aguascalientes': [21.87641043660486, -102.26438663286967],
    'BajaCalifornia': [32.5027, -117.00371],
    'BajaCaliforniaSur': [24.14437, -110.3005],
    'Campeche': [19.8301, -90.53491],
    'Chiapas': [16.75, -93.1167],
    'Chihuahua': [28.6353, -106.0889],
    'CDMX': [19.432713075976878, -99.13318344772986],
    'Coahuila': [25.4260, -101.0053],
    'Colima': [19.2452, -103.725],
    'Durango': [24.0277, -104.6532],
    'Guanajuato': [21.0190, -101.2574],
    'Guerrero': [17.5506, -99.5024],
    'Hidalgo': [20.1011, -98.7624],
    'Jalisco': [20.6767, -103.3475],
    'Mexico': [19.285, -99.5496],
    'Michoacan': [19.701400113725654, -101.20829680213464],
    'Morelos': [18.6813, -99.1013],
    'Nayarit': [21.5085, -104.895],
    'NuevoLeon': [25.6714, -100.309],
    'Oaxaca': [17.0732, -96.7266],
    'Puebla': [19.0414, -98.2063],
    'Queretaro': [20.5972, -100.387],
    'QuintanaRoo': [21.1631, -86.8023],
    'SanLuisPotosi': [22.1565, -100.9855],
    'Sinaloa': [24.8091, -107.394],
    'Sonora': [29.0729, -110.9559],
    'Tabasco': [17.9892, -92.9475],
    'Tamaulipas': [25.4348, -99.134],
    'Tlaxcala': [19.3181, -98.2375],
    'Veracruz': [19.1738, -96.1342],
    'Yucatan': [20.967, -89.6237],
    'Zacatecas': [22.7709, -102.5833]
}

# Calcular la distancia euclidiana entre dos puntos
def calcular_distancia(coord1, coord2):
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

# Implementar el algoritmo de Dijkstra
def dijkstra(grafo, origen, destino):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    predecesores = {nodo: None for nodo in grafo}
    nodos_no_visitados = set(grafo)

    while nodos_no_visitados:
        # Seleccionar el nodo no visitado con la distancia mínima
        nodo_actual = min(nodos_no_visitados, key=lambda nodo: distancias[nodo])

        if distancias[nodo_actual] == float('inf'):
            break  # Todos los nodos alcanzables han sido visitados

        # Para cada vecino del nodo actual
        for vecino, peso in grafo[nodo_actual].items():
            nueva_distancia = distancias[nodo_actual] + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual

        nodos_no_visitados.remove(nodo_actual)

    # Reconstruir el camino desde el destino al origen
    camino = []
    paso_actual = destino
    while paso_actual is not None:
        camino.insert(0, paso_actual)
        paso_actual = predecesores[paso_actual]

    if distancias[destino] == float('inf'):
        return "No hay camino disponible", []

    return camino, distancias[destino]

# Crear el grafo como un diccionario
grafo = {ciudad: {} for ciudad in coord}

for ciudad1 in coord:
    for ciudad2 in coord:
        if ciudad1 != ciudad2:
            distancia = calcular_distancia(coord[ciudad1], coord[ciudad2])
            grafo[ciudad1][ciudad2] = distancia

@app.route('/')
def index():
    return render_template('index.html', ciudades=coord.keys())

@app.route('/get_routes', methods=['POST'])
def get_routes():
    data = request.get_json()
    origen = data['start']
    destino = data['end']

    if origen not in coord or destino not in coord:
        return jsonify({'error': 'Origen o destino no válidos.'}), 400

    # Encontrar el camino más corto usando Dijkstra
    camino, distancia = dijkstra(grafo, origen, destino)

    if isinstance(camino, str):
        return jsonify({'error': camino}), 400

    # Convertir la ruta en coordenadas
    coordenadas_ruta = [coord[ciudad] for ciudad in camino]

    # Retornar el camino y las coordenadas para la visualización en el mapa
    return jsonify({
        'camino': " -> ".join(camino),
        'coordenadas_ruta': coordenadas_ruta,
        'nodos_intermedios_encontrados': camino[1:-1],
        'distancia': distancia
    })

if __name__ == '__main__':
    app.run(debug=True)
