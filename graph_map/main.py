import dijkstra_algorithm
import bellman_ford_algorithm
import floyd_warshall_algorithm

if __name__ == '__main__':
    g = dijkstra_algorithm.Graph(10)
    g.add_vertex_data(0, 'C')
    g.add_vertex_data(1, 'D')
    g.add_vertex_data(2, 'E')
    g.add_vertex_data(3, 'F')
    g.add_vertex_data(4, 'G')
    g.add_vertex_data(5, 'H')

    g.add_edge(0, 1, 3)
    g.add_edge(0, 2, 2)
    g.add_edge(1, 3, 4)
    g.add_edge(2, 1, 1)
    g.add_edge(2, 4, 3)
    g.add_edge(2, 3, 2)
    g.add_edge(3, 4, 2)
    g.add_edge(3, 5, 1)
    g.add_edge(4, 5, 2)

    print("The Dijkstra's Algorithm starting from vertex C to H:")
    distances, predecessors = g.dijkstra('C','H')
    path, cost = g.show_path_from_src_to_dest(distances, predecessors)
    print(f"{path}, Distance: {cost}")
    print("Yen's Algorithm for 3 shortest path from vertex C to H:")
    A = g.yen_ksp(path, cost)
    for item in A:
        print(f"{item['path']}, Distance: {item['cost']}")

    # print("##################################################\n")
    #
    # g = bellman_ford_algorithm.Graph(10)
    # print("The Bellman-Ford's Algorithm starting from vertex D to F:")
    # negative_cycle, distances, predecessors = g.bellman_ford('D', 'F')
    # g.show_path_from_src_to_dest(negative_cycle, distances, predecessors)
    # print("##################################################\n")
    #
    # g = floyd_warshall_algorithm.Graph(10)
    # print("The Floyd-Warshall's Algorithm starting from vertex D to F:")
    # matrix = g.floyd_warshall('D', 'F')
    # g.show_path_from_src_to_dest(matrix)
    #
    exit(0)

