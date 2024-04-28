import json


def load_graph():
    data = None
    source = dict()
    with open("graph_map/data/graph.json", 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    for i in data['nodes']:
        source[str(i['_DataPoint__id'])] = i['_DataPoint__address']

    return source, data['edges'], data['distances']

if __name__ == '__main__':
    source, edges, distances = load_graph()
    print(source)
    print(edges)
    print(distances)