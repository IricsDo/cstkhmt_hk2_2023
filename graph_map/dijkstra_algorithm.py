# https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php

class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  # For undirected graph

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, start_vertex_data, end_vertex_data = None):
        self.start_vertex = start_vertex_data
        self.end_vertex = end_vertex_data
        start_vertex = self.vertex_data.index(start_vertex_data)
        end_vertex = self.vertex_data.index(end_vertex_data)
        distances = [float('inf')] * self.size
        predecessors = [None] * self.size
        distances[start_vertex] = 0
        visited = [False] * self.size

        for _ in range(self.size):
            min_distance = float('inf')
            u = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    u = i

            if u is None or u == end_vertex:
                # print(f"Breaking out of loop. Current vertex: {self.vertex_data[u]}")
                break

            visited[u] = True
            # print(f"Visited vertex: {self.vertex_data[u]}")

            for v in range(self.size):
                if self.adj_matrix[u][v] != 0 and not visited[v]:
                    alt = distances[u] + self.adj_matrix[u][v]
                    if alt < distances[v]:
                        distances[v] = alt
                        predecessors[v] = u

        return distances, predecessors

    def make_path(self, predecessors, start_vertex, end_vertex):
        path = []
        current = self.vertex_data.index(end_vertex)
        while current is not None:
            path.insert(0, self.vertex_data[current])
            current = predecessors[current]
            if current == self.vertex_data.index(start_vertex):
                path.insert(0, start_vertex)
                break
        return '->'.join(path)  # Join the vertices with '->'

    def show_path_from_src_to_dest(self, distances, predecessors):
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