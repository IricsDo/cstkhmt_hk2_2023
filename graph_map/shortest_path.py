import pathlib
import sys

sys.path.insert(0, pathlib.Path(__file__).parent.resolve())

import algorithm.dijkstra_algorithm as dijkstra_algorithm
import algorithm.bellman_ford_algorithm as bellman_ford_algorithm
import algorithm.floyd_warshall_algorithm as floyd_warshall_algorithm
import map.build_graph as bgraph
import random
import aws.loader as aloader
import threading
import concurrent.futures
import time
import datetime
import geojson
import folium
import networkx as nx
from shapely.geometry import Point, LineString

class I_Graph():
    def __init__(self) -> None:
        self.id_dict = dict()
        self.lat_long_dict = dict()
        self.vertexs = list()
        self.edges = list()
        self.list_algo = list()
        self.G = nx.Graph()

    def get_nodes(self):
        return len(self.id_dict.keys())
    
    def load_graph(self, path):
        graphs = bgraph.graph(path)
        self.id_dict, self.lat_long_dict, self.vertexs, self.edges = graphs[0]
        self.G = graphs[1]

    def info_graph(self):
        print("Number of nodes:", self.G.number_of_nodes())
        print("Number of edges:", self.G.number_of_edges())

    def method_build_graph(self, g):
        for j in self.vertexs:
            g.add_vertex_data(j[0], j[1])
        for k in self.edges:
            g.add_edge(int(k[0]), int(k[1]), k[2])
        g.deep_copy_org_graph()

    def load_algorithm(self):
            no_nodes = self.get_nodes()
            self.list_algo = [dijkstra_algorithm.Graph(no_nodes), bellman_ford_algorithm.Graph(no_nodes), floyd_warshall_algorithm.Graph(no_nodes)]
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.list_algo)) as pool:
                    for g in self.list_algo:
                        pool.submit(self.method_build_graph, g)
            except Exception as e:
                print(e)

    def run_dijkstra(self, start_vertex, end_vertex, is_top_K = False, show_result = True):
        distances, predecessors = self.list_algo[0].dijkstra(start_vertex,end_vertex)
        path, cost = self.list_algo[0].show_path_from_src_to_dest(distances, predecessors)
        if path == 'None' or cost == float('inf'):
            return []
        
        if show_result:
            print(f"\nThe Dijkstra's Algorithm starting result:")
            print(f"Path: {path}, Distance: {cost} meters")

        line_paths = list()
        
        if is_top_K:
            paths = list()
            print(f"Yen's Algorithm for 3 shortest path:")
            A = self.list_algo[0].yen_ksp(path, cost)
            for item in A:
                if show_result:
                    print(f"{item['path']}, Distance: {item['cost']}")
                paths.append(item['path'])
            for p in paths:
                line_paths.append(self.get_line_from_path(p))
        else:
            line_paths.append(self.get_line_from_path(path.split('->')))

        return line_paths

    def run_bellman_ford(self, start_vertex, end_vertex, is_top_K=False, show_result = True):
        negative_cycle, distances, predecessors = self.list_algo[1].bellman_ford(start_vertex, end_vertex)
        path, cost = self.list_algo[1].show_path_from_src_to_dest(negative_cycle, distances, predecessors)
        if path == 'None' or cost == float('inf'):
            return []
        
        if show_result:
            print(f"\nThe Bellman-Ford's Algorithm result:")
            print(f"Path: {path}, Distance: {cost} meters")

        line_paths = list()

        if is_top_K:
            paths = list()
            print(f"Yen's Algorithm for 3 shortest path:")
            A = self.list_algo[1].yen_ksp(path, cost)
            for item in A:
                if show_result:
                    print(f"{item['path']}, Distance: {item['cost']}")
                paths.append(item['path'])
            line_paths = list()
            for p in paths:
                line_paths.append(self.get_line_from_path(p))
        else:
            line_paths.append(self.get_line_from_path(path.split('->')))

        return line_paths

    def run_floyd_warshall(self, start_vertex, end_vertex, is_top_K=False, show_result = True):
        matrix = self.list_algo[2].floyd_warshall(start_vertex, end_vertex)
        path, cost = self.list_algo[2].show_path_from_src_to_dest(matrix)
        if path == 'None' or cost == float('inf'):
            return []
        if show_result:
            print(f"\nThe Floyd-Warshall's Algorithm result")
            print(f"Path: {path}, Distance: {cost} meters")
        
        line_paths = list()

        if is_top_K:
            paths = list()
            print(f"Yen's Algorithm for 3 shortest path:")
            A = self.list_algo[2].yen_ksp(path, cost)
            for item in A:
                if show_result:
                    print(f"{item['path']}, Distance: {item['cost']}")
                paths.append(item['path'])
            for p in paths:
                line_paths.append(self.get_line_from_path(p))
        else:
            line_paths.append(self.get_line_from_path(path.split('->')))

        return line_paths

    def run_parallel(self, start_vertex=0, end_vertex=0, is_top_K=False, show_result = True):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.list_algo)) as pool:
                pool.submit(self.run_dijkstra, start_vertex, end_vertex, is_top_K, show_result)
                pool.submit(self.run_bellman_ford, start_vertex, end_vertex, is_top_K, show_result)
                pool.submit(self.run_floyd_warshall, start_vertex, end_vertex, is_top_K, show_result)
        except Exception as e:
            print(e)
    
    def run_sequence(self, algorithm, start_vertex=0, end_vertex=0, is_top_K=False, show_result = True):
        result = None
        if algorithm == 'dijkstra':
            result = self.run_dijkstra(start_vertex, end_vertex, is_top_K, show_result)
        elif algorithm == 'bellman_ford':
            result = self.run_bellman_ford(start_vertex, end_vertex, is_top_K, show_result)
        elif algorithm == 'floyd_warshall':
            result = self.run_floyd_warshall(start_vertex, end_vertex, is_top_K, show_result)

        return result
    
    def get_line_from_path(self,path):
        coord_list = list()
        array= [self.id_dict[point] for point in path]
        for i in range(len(array)):
            lat, long = self.G.nodes[array[i]]['latitude'], self.G.nodes[array[i]]['longitude']
            coord_list.append((long, lat))

        point_objects = [Point(x, y) for x, y in coord_list]
        line = LineString(point_objects)
        geojson_line = geojson.LineString(line.coords)

        return geojson_line

    def find_nearest_lat_long(self, lat : float, long : float):
        lat_long = self.lat_long_dict.values()
        nearest = min(lat_long, key=lambda x: (abs(x[0] - lat), abs(x[1] - long)))
        id = list(self.lat_long_dict.keys())[list(self.lat_long_dict.values()).index(nearest)]

        return (lat, long), nearest, id

    def user_input(self):
        print('Enter lat, long | Example xxx.000000, yyy.000000')
        while True:
            start_vertex  = input('Start vertex input: ')
            end_vertex  = input('End vertex input: ')

            start_vertex = str(start_vertex).replace(" ", "")
            end_vertex = str(end_vertex).replace(" ", "")

            lat_long_sv = start_vertex.split(',')
            lat_long_ev = end_vertex.split(',')

            if not all(isinstance(float(x), float) for x in lat_long_sv) or  not all(isinstance(float(x), float) for x in lat_long_ev):
                print('Wrong type, try again !')
            else:
                break

        return lat_long_sv, lat_long_ev

if __name__ == '__main__':

    slo = None
    with aloader.Loader("Loading alogrithm...", "Algorithm already!"):
        slo = I_Graph()
        slo.load_graph('graph_map/data/Road/Co_Giang_Road.geojson')
        slo.load_algorithm()

    print('\n')
    slo.info_graph()
    print('\n')

    # result = slo.find_nearest_lat_long(10.762347, 106.693725)
    # print('From google map:', result[0])
    # print('From database:', result[1], '| id:', result[2])

    # slo.user_input()

    print('Done')
    print('\n')
    exit(0)