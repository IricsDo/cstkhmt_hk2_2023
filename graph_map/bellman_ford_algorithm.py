# ********* Reference link *********

# https://www.w3schools.com/dsa/dsa_algo_graphs_bellmanford.php
# The Yen's Algorithm has been implemented by following the dijkstra_algorithm
class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            #self.adj_matrix[v][u] = weight  # For undirected graph

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def bellman_ford(self, start_vertex_data, end_vertex_data = None):
        self.start_vertex = start_vertex_data
        self.end_vertex = end_vertex_data
        start_vertex = self.vertex_data.index(start_vertex_data)
        distances = [float('inf')] * self.size
        predecessors = [None] * self.size
        distances[start_vertex] = 0

        for i in range(self.size - 1):
            for u in range(self.size):
                for v in range(self.size):
                    if self.adj_matrix[u][v] != 0:
                        if distances[u] + self.adj_matrix[u][v] < distances[v]:
                            distances[v] = distances[u] + self.adj_matrix[u][v]
                            predecessors[v] = u
                            # print(f"Relaxing edge {self.vertex_data[u]}->{self.vertex_data[v]}, Updated distance to {self.vertex_data[v]}: {distances[v]}")

        # Negative cycle detection
        for u in range(self.size):
            for v in range(self.size):
                if self.adj_matrix[u][v] != 0:
                    if distances[u] + self.adj_matrix[u][v] < distances[v]:
                        return (True, None, None)  # Indicate a negative cycle was found
        
        return (False, distances, predecessors)  # Indicate no negative cycle and return distances
    
    def make_path(self, predecessors, start_vertex, end_vertex):
        path = []
        current = self.vertex_data.index(end_vertex)
        while current is not None:
            path.insert(0, self.vertex_data[current])
            current = predecessors[current]
            if current == self.vertex_data.index(start_vertex):
                path.insert(0, start_vertex)
                break
        return '->'.join(path)
    
    def show_path_from_src_to_dest(self, negative_cycle, distances, predecessors):
        if not negative_cycle:
            if not self.end_vertex:
                for i, d in enumerate(distances):
                    if d != float('inf'):
                        path = self.make_path(predecessors, self.start_vertex, self.vertex_data[i])
                        print(f"{path}, Distance: {d}")
                    else:
                        print(f"No path from D to {self.vertex_data[i]}, Distance: Infinity")
            else:
                path = self.make_path(predecessors, self.start_vertex, self.end_vertex)
                d = distances[self.vertex_data.index(self.end_vertex)]
                print(f"{path}, Distance: {d}")

        else:
            print("Negative weight cycle detected. Cannot compute shortest paths.")

    