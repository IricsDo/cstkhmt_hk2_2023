
# https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/
# https://www.geeksforgeeks.org/finding-shortest-path-between-any-two-nodes-using-floyd-warshall-algorithm/


class Graph:
    def __init__(self, size) -> None:
        # Number of vertices in the graph
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = ['']*size
        # Define infinity as the large
        # enough value. This value will be
        # used for vertices not connected to each other

        MAXM,self.INF = 100,10**7
        self.dist = [[-1 for i in range(MAXM)] for i in range(MAXM)]
        self.Next = [[-1 for i in range(MAXM)] for i in range(MAXM)]

    # Initializing the distance and
    # Next array
    # def initialise(self, graph):
    #     for i in range(self.V):
    #         for j in range(self.V):
    #             self.dist[i][j] = graph[i][j]
    
    #             # No edge between node
    #             # i and j
    #             if (graph[i][j] == self.INF):
    #                 self.Next[i][j] = -1
    #             else:
    #                 self.Next[i][j] = j
    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            if (weight == self.INF):
                self.Next[u][v] = -1
            else:
                self.Next[u][v] = weight

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def floyd_warshall(self, graph):

        # self.initialise(graph)

        """ dist[][] will be the output 
        matrix that will finally
            have the shortest distances 
            between every pair of vertices """
        """ initializing the solution matrix 
        same as input graph matrix
        OR we can say that the initial 
        values of shortest distances
        are based on shortest paths considering no 
        intermediate vertices """

        # dist = list(map(lambda i: list(map(lambda j: j, i)), graph))

        """ Add all vertices one by one 
        to the set of intermediate
        vertices.
        ---> Before start of an iteration, 
        we have shortest distances
        between all pairs of vertices 
        such that the shortest
        distances consider only the 
        vertices in the set 
        {0, 1, 2, .. k-1} as intermediate vertices.
        ----> After the end of a 
        iteration, vertex no. k is
        added to the set of intermediate 
        vertices and the 
        set becomes {0, 1, 2, .. k}
        """
        for k in range(self.size):
            # pick all vertices as source one by one
            for i in range(self.size):
                # Pick all vertices as destination for the
                # above picked source
                for j in range(self.size):
                    # We cannot travel through
                     # edge that doesn't exist
                    if (self.dist[i][k] == self.INF or self.dist[k][j] == self.INF):
                        continue

                    if (self.dist[i][j] > self.dist[i][k] + self.dist[k][j]):
                        # If vertex k is on the shortest path from
                        # i to j, then update the value of dist[i][j]
                        self.dist[i][j] = min(self.dist[i][j],
                                        self.dist[i][k] + self.dist[k][j]
                                        )
                        self.Next[i][j] = self.Next[i][k]

        # self.printSolution(self.dist)

    # Function construct the shortest
    # path between u and v
    def constructPath(self, u, v):        
        # If there's no path between
        # node u and v, simply return
        # an empty array
        if (self.Next[u][v] == -1):
            return {}
    
        # Storing the path in a vector
        path = [u]
        while (u != v):
            u = self.Next[u][v]
            path.append(u)
    
        return path
    

    # Print the shortest path
    def printPath(self, path):
        n = len(path)
        for i in range(n - 1):
            print(path[i], end=" -> ")
        print(path[n - 1])

    # A utility function to print the solution
    def printSolution(self, dist):
        print("Following matrix shows the shortest distances\
    between every pair of vertices")
        for i in range(self.V):
            for j in range(self.V):
                if(dist[i][j] == self.INF):
                    print("%7s" % ("INF"), end=" ")
                else:
                    print("%7d\t" % (dist[i][j]), end=' ')
                if j == self.V-1:
                    print()


# Driver's code
if __name__ == "__main__":
    """
                10
           (0)------->(3)
            |         /|\
          5 |          |
            |          | 1
           \|/         |
           (1)------->(2)
                3           """

    g = Graph(4)
    graph = [[0, 5, g.INF, 10],
            [g.INF, 0, 3, g.INF],
            [g.INF, g.INF, 0,   1],
            [g.INF, g.INF, g.INF, 0]
            ]
    g.floyd_warshall(graph)
    path = []

    # Path from node 1 to 3
    print("Shortest path from 1 to 3: ", end = "")
    path = g.constructPath(1, 3)
    g.printPath(path)
