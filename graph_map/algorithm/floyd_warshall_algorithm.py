# ********* Reference link *********

# https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/
# https://www.geeksforgeeks.org/finding-shortest-path-between-any-two-nodes-using-floyd-warshall-algorithm/
# The Yen's Algorithm has been implemented by following the dijkstra_algorithm

from collections import OrderedDict
import copy


class Graph:
    def __init__(self, size) -> None:
        self.org_matrix = None
        self.end_vertex = None
        self.start_vertex = None
        self.INF = float('inf')
        self.size = size
        self.vertex_data = [''] * size
        self.adj_matrix = [[self.INF] * size for _ in range(size)]
        self.next_matrix = [[-1] * size for _ in range(size)]
        self.org_next = list()

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            #self.adj_matrix[v][u] = weight  # For undirected graph
            self.adj_matrix[u][u] = 0
            self.adj_matrix[v][v] = 0
            self.next_matrix[u][v] = v
            self.next_matrix[u][u] = u
            self.next_matrix[v][v] = v


    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def deep_copy_org_graph(self):
        self.org_matrix = copy.deepcopy(self.adj_matrix)
        self.org_next = copy.deepcopy(self.next_matrix)

    def floyd_warshall(self, start_vertex, end_vertex=None):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.adj_matrix = copy.deepcopy(self.org_matrix)
        self.next_matrix = copy.deepcopy(self.org_next)
        # print(f"L0")
        # self.print_solution(self.org_matrix)
        for k in range(1, self.size):
            for i in range(self.size):
                for j in range(self.size):
                    # We cannot travel through edge that doesn't exist
                    value_hori = self.adj_matrix[i][k - 1]
                    value_verti = self.adj_matrix[k - 1][j]
                    if value_hori == self.INF or value_verti == self.INF:
                        continue
                    value_curr = self.adj_matrix[i][j]
                    if value_curr > value_hori + value_verti:
                        # If vertex k is on the shortest path from
                        # i to j, then update the value
                        self.adj_matrix[i][j] = value_hori + value_verti
                        self.next_matrix[i][j] = self.next_matrix[i][k - 1]

            # print(f"L{k}")
            # self.print_solution(self.adj_matrix)
        # self.print_solution(self.org_matrix)
        return self.construct_path(start_vertex, end_vertex)

    # Function construct the shortest
    # path between u and v
    def construct_path(self, u, v):
        # If there's no path between
        # node u and v, simply return
        # an empty array
        u_index = self.vertex_data.index(u)
        v_index = self.vertex_data.index(v)
        if self.next_matrix[u_index][v_index] == -1:
            # print(f'Can not find the path for {u} and {v}')
            return list()
        path = list()
        # Storing the path in a vector
        path = [u_index]
        while u_index != v_index:
            u_index = self.next_matrix[u_index][v_index]
            path.append(u_index)

        return path

    # Print the shortest paths
    def show_path_from_src_to_dest(self, matrix):
        n = len(matrix)
        if n == 0:
            return 'None', 'inf'
        d = 0
        list_vertex = list()
        for i in range(n - 1):
            list_vertex.append(self.vertex_data[matrix[i]])
        list_vertex.append(self.vertex_data[matrix[n - 1]])
        for i in range(len(list_vertex) - 1):
            d += self.org_matrix[self.vertex_data.index(list_vertex[i])][self.vertex_data.index(list_vertex[i + 1])]
        return '->'.join(list_vertex), d

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

    def yen_ksp(self, S, C, K=3):
        # Determine the shortest path from the source to the destination.
        k_shortest_path = [{'cost': C, 'path': S.split("->")}]
        # Initialize the set to store the potential kth shortest path.
        potential_shortest_path = []
        for k in range(1, K):
            # The spur node ranges from the first node to the next to last node in the previous k-shortest path.
            for i in range(0, len(k_shortest_path[k - 1]['path']) - 1):
                # Spur node is retrieved from the previous k-shortest path, k − 1.
                spur_node = k_shortest_path[k - 1]['path'][i]
                # The sequence of nodes from the source to the spur node of the previous k-shortest path.
                root_path = k_shortest_path[k - 1]['path'][:i + 1]
                list_remove_link = []
                next_link = []
                for p in k_shortest_path:
                    curr_path = p['path']
                    if root_path == curr_path[: i + 1]:
                        cost = 0
                        next_path = ''
                        # Remove the links that are part of the previous shortest paths which share the same root path.
                        first_index = self.vertex_data.index(curr_path[i])
                        last_index = self.vertex_data.index(curr_path[i + 1])
                        cost = self.org_matrix[first_index][last_index]
                        next_path = self.org_next[first_index][last_index]
                        if cost == self.INF:
                            continue
                        list_remove_link.append([first_index, last_index, cost])
                        next_link.append([first_index, last_index, next_path])
                        next_link.append([first_index, first_index, first_index])
                        self.org_matrix[first_index][last_index] = self.INF
                        self.org_next[first_index][last_index] = -1

                # for rootPathNode in rootPath:
                # if rootPathNode != spurNode:
                # remove rootPathNode from Graph;
                # pass
                '''
                      Don't need to implement the code remove node from graph, because we search from root_path, not in all node in graph
                '''

                # Calculate the spur path from the spur node to the sink.
                # Consider also checking if any spurPath found

                matrix = self.floyd_warshall(root_path[-1], self.end_vertex)
                path, cost = self.show_path_from_src_to_dest(matrix)
                if cost == self.INF:
                    break
                spur_path = path.split("->")
                # Entire path is made up of the root path and spur path.
                total_path = list(OrderedDict.fromkeys(root_path + spur_path))
                pre_cost = 0
                if len(root_path) > i != 0:
                    for c in range(0, len(root_path) - 1):
                        pre_cost += self.org_matrix[self.vertex_data.index(root_path[c])][
                            self.vertex_data.index(root_path[c + 1])]
                total_cost = float(cost) + float(pre_cost)
                potential_k = {'cost': total_cost, 'path': total_path}
                # Add the potential k-shortest path to the heap.
                if not (potential_k in potential_shortest_path):
                    potential_shortest_path.append(potential_k)

                # Add back the edges and nodes that were removed from the graph.
                for l in list_remove_link:
                    self.org_matrix[l[0]][l[1]] = l[2]
                for n in next_link:
                    self.org_next[n[0]][n[1]] = n[2]

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
