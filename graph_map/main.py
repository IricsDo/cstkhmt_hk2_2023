import pathlib
import sys

sys.path.insert(0, pathlib.Path(__file__).parent.resolve())

import dijkstra_algorithm
import bellman_ford_algorithm
import floyd_warshall_algorithm
import map.build_graph as bgraph
import random
import aws.loader as aloader
import threading
import concurrent.futures
import time
import datetime
import geojson
import folium
from shapely.geometry import Point, LineString

class I_Graph():
    def __init__(self) -> None:
        self.id_dict = dict()
        self.vertexs = list()
        self.edges = list()
        self.list_algo = list()
        self.G = None

    def get_nodes(self):
        return len(self.id_dict.keys())
    
    def load_graph(self):
        graphs = bgraph.graph()
        self.id_dict, self.vertexs, self.edges = graphs[0]
        self.G = graphs[1]

    def method_build_graph(self, g):
        for j in self.vertexs:
            g.add_vertex_data(j[0], j[1])
        for k in self.edges:
            g.add_edge(int(k[0]), int(k[1]), k[2])
        g.deep_copy_org_graph()

    def load_algorithm(self):
        no_nodes = len(self.id_dict.keys())
        self.list_algo = [dijkstra_algorithm.Graph(no_nodes), bellman_ford_algorithm.Graph(no_nodes), floyd_warshall_algorithm.Graph(no_nodes)]
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(self.list_algo))
        try:
            for g in self.list_algo:
                pool.submit(self.method_build_graph, g)
            pool.shutdown(wait=True)
        except Exception as e:
            pool.shutdown(wait=False)

    def method_run_dijkstra(self, algo, start_vertex, end_vertex, is_top_K = False):
        distances, predecessors = algo.dijkstra(start_vertex,end_vertex)
        path, cost = algo.show_path_from_src_to_dest(distances, predecessors)
        print(f"\nThe Dijkstra's Algorithm starting result:")
        print(f"Path: {path}, Distance: {cost} meters")

        if is_top_K:
            print(f"Yen's Algorithm for 3 shortest path:")
            A = algo.yen_ksp(path, cost)
            for item in A:
                print(f"{item['path']}, Distance: {item['cost']}")

        pathList = path.split('->')
        return self.getLineFromPath(pathList)
    
    def method_run_bellman_ford(self, algo, start_vertex, end_vertex, is_top_K=False):
        negative_cycle, distances, predecessors = algo.bellman_ford(start_vertex, end_vertex)
        path, cost = algo.show_path_from_src_to_dest(negative_cycle, distances, predecessors)
        print(f"\nThe Bellman-Ford's Algorithm result:")
        print(f"Path: {path}, Distance: {cost} meters")

        coordinates = [bgraph.get_coordinates(str(point),bgraph.G) for point in path]
        print(f"Coordinates: {coordinates}")

        if is_top_K:
            print(f"Yen's Algorithm for 3 shortest path:")
            A = algo.yen_ksp(path, cost)
            for item in A:
                print(f"{item['path']}, Distance: {item['cost']} meters")
        
        pathList = path.split('->')
        return self.getLineFromPath(pathList)

    def method_run_floyd_warshall(self, algo, start_vertex, end_vertex, is_top_K=False):
        matrix = algo.floyd_warshall(start_vertex, end_vertex)
        path, cost = algo.show_path_from_src_to_dest(matrix)
        print(f"\nThe Floyd-Warshall's Algorithm result")
        print(f"Path: {path}, Distance: {cost} meters")

        if is_top_K:
            print(f"Yen's Algorithm for 3 shortest path:")
            A = algo.yen_ksp(path, cost)
            for item in A:
                print(f"{item['path']}, Distance: {item['cost']} meters")
        
        pathList = path.split('->')
        return self.getLineFromPath(pathList)

    def run_dijkstra(self, start_vertex=0, end_vertex=0, is_top_K=False):
        return self.method_run_dijkstra(self.list_algo[0], start_vertex, end_vertex, is_top_K)

    def run_bellman_ford(self, start_vertex=0, end_vertex=0, is_top_K=False):
        return self.method_run_bellman_ford(self.list_algo[1], start_vertex, end_vertex, is_top_K)

    def run_floyd_warshall(self, start_vertex=0, end_vertex=0, is_top_K=False):
        return self.method_run_floyd_warshall(self.list_algo[2], start_vertex, end_vertex, is_top_K)
         
    def run(self, start_vertex=0, end_vertex=0, is_top_K=False):
        try:
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(self.list_algo))
            for i in range(len(self.list_algo)):
                if i == 0:
                    pool.submit(self.method_run_dijkstra, self.list_algo[i], start_vertex, end_vertex, is_top_K)
                elif i == 1:
                    pool.submit(self.method_run_bellman_ford, self.list_algo[i], start_vertex, end_vertex, is_top_K)
                elif i == 2:
                    pool.submit(self.method_run_floyd_warshall, self.list_algo[i], start_vertex, end_vertex, is_top_K)
            pool.shutdown(wait=True)
        except Exception as e:
            pool.shutdown(wait=False)
    
    def getLineFromPath(self,path):
        coord_list = list()
        array= [self.id_dict[point] for point in path]
        for i in range(len(array)):
            lat, long = self.G.nodes[array[i]]['latitude'], self.G.nodes[array[i]]['longitude']
            coord_list.append((long, lat))

        point_objects = [Point(x, y) for x, y in coord_list]
        line = LineString(point_objects)
        geojson_line = geojson.LineString(line.coords)

        return geojson_line

if __name__ == '__main__':
    start_time = time.time()

    slo = None
    with aloader.Loader("Loading alogrithm...", "Algorithm already!"):
        slo = I_Graph()
        slo.load_graph()
        slo.load_algorithm()
    
    start_vertex = str(random.randint(0, slo.get_nodes() - 1))
    end_vertex = str(random.randint(0, slo.get_nodes() - 1))
    start_vertex = 91
    end_vertex = 5422
    print(f"\n===>>> Calculating shortest-path between {start_vertex} and {end_vertex} <<<===")
    print('Please wating ...')
    slo.run(start_vertex, end_vertex, False)

    executed_time = round(time.time() - start_time)
    print("\n\nTime executed: {}".format(str(datetime.timedelta(seconds=executed_time))))

    print('\n')
    exit(0)