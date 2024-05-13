import json
import networkx as nx
from geopy.distance import geodesic

def buildGraph(filePath):
    with open(filePath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        road_segments = []
        for feature in data['features']:
            if feature['geometry']['type'] == 'LineString':
                segment = {
                    'id': feature['properties']['@id'],
                    'nodes': feature['geometry']['coordinates'],
                    'weight': 1  # Placeholder weight for demonstration
                }
                road_segments.append(segment)
    # Construct graph
    G = nx.Graph()
    node_mapping = {}  # Dictionary to map coordinates to node IDs

    for segment in road_segments:
        for i, coordinates in enumerate(segment['nodes']):
            # Check if a node with the same coordinates already exists
            node_id = node_mapping.get(tuple(coordinates))
            if node_id is None:
                # If not, create a new node
                node_id = segment['id'] + '_' + str(i)
                node_mapping[tuple(coordinates)] = node_id
                G.add_node(node_id, id=node_id, latitude=coordinates[1], longitude=coordinates[0])
            else:
                # If yes, use the existing node ID
                node_id = node_id

        for i in range(len(segment['nodes']) - 1):
            u = node_mapping[tuple(segment['nodes'][i])]
            v = node_mapping[tuple(segment['nodes'][i + 1])]
            G.add_edge(u, v)

    # # # Example usage:
    # print("Number of nodes:", G.number_of_nodes())
    # print("Number of edges:", G.number_of_edges())
    return G

def value_to_key(dicts : dict, value):
    return list(dicts.keys())[list(dicts.values()).index(value)]

def buildAdjacencyList(G):
    # Create an empty adjacency list
    adj_list = {}
    id_dict = dict() # {'1': 'some thing name', ...}
    lat_long_dict = dict()
    vertexs = list() # [(1, '1'), (2, '2'), ...]
    edges = list() # [(1, 2, 1000m), (2, 1, 1000m), ...]
    index_id = 0

    # Calculate distances between connected nodes and store them as weights in the adjacency list
    for n in G.nodes():
        if n not in id_dict.values():
            id_dict[str(index_id)] = n
            lat_long_dict[str(index_id)]= (G.nodes[n]['latitude'], G.nodes[n]['longitude'])
            index_id += 1

    for key in id_dict.keys(): 
        vertexs.append((int(key), key))

    for u, v in G.edges():
        node_u = G.nodes[u]
        node_v = G.nodes[v]
        distance = geodesic((node_u['latitude'], node_u['longitude']), (node_v['latitude'], node_v['longitude'])).meters

        # Add edge (v, weight) to the adjacency list of node u
        if u not in adj_list:
            adj_list[u] = [(v, distance)]
        else:
            adj_list[u].append((v, distance))
        # Add edge (u, weight) to the adjacency list of node v
        if v not in adj_list:
            adj_list[v] = [(u, distance)]
        else:
            adj_list[v].append((u, distance))

    # Print the adjacency list
    for node, neighbors in adj_list.items():
        start_vertex = int(value_to_key(id_dict, node))
        for k in neighbors:
            end_vertex = int(value_to_key(id_dict, k[0]))
            edges.append((start_vertex, end_vertex, k[1]))

    return id_dict, lat_long_dict, vertexs, edges

def graph(geoJsonPath):
    G = buildGraph(geoJsonPath)
    return [buildAdjacencyList(G), G]

if __name__ == "__main__":
    graphs = graph('graph_map/data/Road/Co_Giang_Road.geojson')
    id_dict, lat_long_dict, vertexs, edges = graphs[0]
    print('id_dict', len(id_dict))
    print('lat_long_dict', len(lat_long_dict))
    print('vertexs', len(vertexs))
    print('edges', len(edges))

    exit(0)