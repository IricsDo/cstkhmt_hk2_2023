# ********* Reference link *********

# https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php
# https://en.wikipedia.org/wiki/Yen%27s_algorithm
# https://people.csail.mit.edu/minilek/yen_kth_shortest.pdf
# https://github.com/handloomweaver/YenKSP/blob/master/algorithms.py

from collections import OrderedDict
import copy
class Graph:
    def __init__(self, size):
        self.end_vertex = None
        self.start_vertex = None
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.org_matrix = None
        self.size = size
        self.vertex_data = [''] * size
        self.INF = 10**7

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            # self.adj_matrix[v][u] = weight  # For undirected graph
            self.org_matrix = copy.deepcopy(self.adj_matrix)

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, start_vertex_data, end_vertex_data=None):
        self.start_vertex = start_vertex_data
        self.end_vertex = end_vertex_data
        start_vertex = self.vertex_data.index(start_vertex_data)
        end_vertex = self.vertex_data.index(end_vertex_data)
        distances = [float('inf')] * self.size
        predecessors = [None] * self.size
        distances[start_vertex] = 0
        visited = [False] * self.size
        self.adj_matrix = copy.deepcopy(self.org_matrix)

        for _ in range(self.size):
            min_distance = float('inf')
            u = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance and distances[i] != self.INF:
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
        path = ''
        d = self.INF
        if not self.end_vertex:
            for i, d in enumerate(distances):
                if d != float('inf'):
                    path = self.make_path(predecessors, self.start_vertex, self.vertex_data[i])
                else:
                    print(f"No path from D to {self.vertex_data[i]}, Distance: Infinity")
        else:
            path = self.make_path(predecessors, self.start_vertex, self.end_vertex)
            d = distances[self.vertex_data.index(self.end_vertex)]
        return path, d

    def yen_ksp(self, S, C, K=3):
        # Determine the shortest path from the source to the destination.
        k_shortest_path = [{'cost': C, 'path': S.split("->")}]
        # Initialize the set to store the potential kth shortest path.
        potential_shortest_path = []
        for k in range(1, K):
            # The spur node ranges from the first node to the next to last node in the previous k-shortest path.
            for i in range(0, len(k_shortest_path[k-1]['path']) - 1):
                # Spur node is retrieved from the previous k-shortest path, k − 1.
                spur_node = k_shortest_path[k - 1]['path'][i]
                # The sequence of nodes from the source to the spur node of the previous k-shortest path.
                root_path = k_shortest_path[k - 1]['path'][:i+1]

                list_remove_link = []
                for p in k_shortest_path:
                    curr_path = p['path']
                    if root_path == curr_path[: i+1]:
                        # Remove the links that are part of the previous shortest paths which share the same root path.
                        first_index = self.vertex_data.index(curr_path[i])
                        last_index = self.vertex_data.index(curr_path[i+1])
                        cost = self.org_matrix[first_index][last_index]
                        if cost == self.INF:
                            continue
                        list_remove_link.append([first_index, last_index, cost])
                        self.org_matrix[first_index][last_index] = self.INF

                # for rootPathNode in rootPath:
                    # if rootPathNode != spurNode:
                        # remove rootPathNode from Graph;
                        # pass
                '''
                      Don't need to implement the code remove node from graph, because we search from root_path, not in all node in graph
                '''

                # Calculate the spur path from the spur node to the sink.
                # Consider also checking if any spurPath found

                distances, predecessors = self.dijkstra(root_path[-1], self.end_vertex)
                path, cost = self.show_path_from_src_to_dest(distances, predecessors)
                if cost == self.INF:
                    break
                spur_path = path.split("->")
                # Entire path is made up of the root path and spur path.
                total_path = list(OrderedDict.fromkeys(root_path + spur_path))
                pre_cost = 0
                if len(root_path) > i != 0:
                    for c in range(0, len(root_path) - 1):
                        pre_cost += self.org_matrix[self.vertex_data.index(root_path[c])][self.vertex_data.index(root_path[c+1])]
                total_cost = cost + pre_cost
                potential_k = {'cost': total_cost, 'path': total_path}
                # Add the potential k-shortest path to the heap.
                if not (potential_k in potential_shortest_path):
                    potential_shortest_path.append(potential_k)

                # Add back the edges and nodes that were removed from the graph.
                for l in list_remove_link:
                    self.org_matrix[l[0]][l[1]] = l[2]

                # restore nodes in rootPath to Graph;

            if len(potential_shortest_path) == 0:
                # This handles the case of there being no spur paths, or no spur paths left.
                # This could happen if the spur paths have already been exhausted (added to A),
                # or there are no spur paths at all - such as when both the source and sink vertices
                # lie along a "dead end".
                break
            # Sort the potential k-shortest paths by cost.
            potential_shortest_path = sorted(potential_shortest_path, key=lambda d: d['cost'])
            if len(k_shortest_path) == K:
                break
            # Add the lowest cost path becomes the k-shortest path.
            k_shortest_path.append(potential_shortest_path[0])
            # In fact we should rather use shift since we are removing the first element
            potential_shortest_path.pop(0)

        return k_shortest_path