# https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/
# https://www.geeksforgeeks.org/finding-shortest-path-between-any-two-nodes-using-floyd-warshall-algorithm/

class Graph:
    def __init__(self, size) -> None:
        self.INF = 10 ** 7
        self.size = size
        self.vertex_data = [''] * size
        self.adj_matrix = [[self.INF] * size for _ in range(size)]
        self.ogr_matrix = None
        self.Next = [[-1] * size for _ in range(size)]

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[u][u] = 0
            self.adj_matrix[v][v] = 0
            self.Next[u][v] = v
            self.Next[u][u] = u
            self.Next[v][v] = v

        self.ogr_matrix = self.adj_matrix

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def floyd_warshall(self, start_vertex, end_vertex):

        for k in range(self.size):
            for i in range(self.size):
                for j in range(self.size):
                    # We cannot travel through edge that doesn't exist
                    if self.adj_matrix[i][k] == self.INF or self.adj_matrix[k][j] == self.INF:
                        continue
                    if self.adj_matrix[i][j] > self.adj_matrix[i][k] + self.adj_matrix[k][j]:
                        # If vertex k is on the shortest path from
                        # i to j, then update the value
                        self.adj_matrix[i][j] = min(self.adj_matrix[i][j],
                                                    self.adj_matrix[i][k] + self.adj_matrix[k][j]
                                                    )
                        self.Next[i][j] = self.Next[i][k]

        # self.print_solution(self.adj_matrix)
        return self.construct_path(start_vertex, end_vertex)

    # Function construct the shortest
    # path between u and v
    def construct_path(self, u, v):
        # If there's no path between
        # node u and v, simply return
        # an empty array
        u_index = self.vertex_data.index(u)
        v_index = self.vertex_data.index(v)
        if self.Next[u_index][v_index] == -1:
            return {}

        # Storing the path in a vector
        path = [u_index]
        while u_index != v_index:
            u_index = self.Next[u_index][v_index]
            path.append(u_index)

        return path

    # Print the shortest paths
    def show_path_from_src_to_dest(self, matrix):
        n = len(matrix)
        if n == 0:
            return self.INF
        d = 0
        list_vertex = list()
        for i in range(n - 1):
            list_vertex.append(self.vertex_data[matrix[i]])
        list_vertex.append(self.vertex_data[matrix[n - 1]])
        for i in range(len(list_vertex) - 1):
            d += self.ogr_matrix[self.vertex_data.index(list_vertex[i])][self.vertex_data.index(list_vertex[i + 1])]
        print(f"{'->'.join(list_vertex)}, Distance: {d}")

    # A utility function to print the solution
    def print_solution(self, dist):
        print("Following matrix shows the shortest distances\
    between every pair of vertices")
        for i in range(self.size):
            for j in range(self.size):
                if dist[i][j] == self.INF:
                    print("%7s" % "INF", end=" ")
                else:
                    print("%7d" % (dist[i][j]), end=' ')
                if j == self.size - 1:
                    print()
