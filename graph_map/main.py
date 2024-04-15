
import dijkstra_algorithm
import bellman_ford_algorithm

if __name__ == '__main__':
    g = dijkstra_algorithm.Graph(10)
    g.add_vertex_data(0, 'A')
    g.add_vertex_data(1, 'B')
    g.add_vertex_data(2, 'C')
    g.add_vertex_data(3, 'D')
    g.add_vertex_data(4, 'E')
    g.add_vertex_data(5, 'F')
    g.add_vertex_data(6, 'G')
    g.add_vertex_data(7, 'H')
    g.add_vertex_data(8, 'I')
    g.add_vertex_data(9, 'J')

    g.add_edge(3, 0, 4)  # D - A, weight 4
    g.add_edge(3, 4, 2)  # D - E, weight 2
    g.add_edge(0, 2, 3)  # A - C, weight 3
    g.add_edge(0, 4, 4)  # A - E, weight 4
    g.add_edge(4, 2, 4)  # E - C, weight 4
    g.add_edge(4, 6, 5)  # E - G, weight 5
    g.add_edge(2, 5, 5)  # C - F, weight 5
    g.add_edge(2, 1, 2)  # C - B, weight 2
    g.add_edge(1, 5, 2)  # B - F, weight 2
    g.add_edge(6, 5, 5)  # G - F, weight 5
    g.add_edge(6, 8, 4)  # G - I, weight 4
    g.add_edge(6, 7, 5)  # G - H, weight 5
    g.add_edge(8, 9, 2)  # I - J, weight 2

    print("The Dijkstra's Algorithm starting from vertex D to F:\n")
    distances, predecessors = g.dijkstra('D','F')
    g.show_path_from_src_to_dest(distances, predecessors)

    print("##################################################")

    g = bellman_ford_algorithm.Graph(10)
    g.add_vertex_data(0, 'A')
    g.add_vertex_data(1, 'B')
    g.add_vertex_data(2, 'C')
    g.add_vertex_data(3, 'D')
    g.add_vertex_data(4, 'E')
    g.add_vertex_data(5, 'F')
    g.add_vertex_data(6, 'G')
    g.add_vertex_data(7, 'H')
    g.add_vertex_data(8, 'I')
    g.add_vertex_data(9, 'J')

    g.add_edge(3, 0, 4)  # D - A, weight 4
    g.add_edge(3, 4, 2)  # D - E, weight 2
    g.add_edge(0, 2, 3)  # A - C, weight 3
    g.add_edge(0, 4, 4)  # A - E, weight 4
    g.add_edge(4, 2, 4)  # E - C, weight 4
    g.add_edge(4, 6, 5)  # E - G, weight 5
    g.add_edge(2, 5, 5)  # C - F, weight 5
    g.add_edge(2, 1, 2)  # C - B, weight 2
    g.add_edge(1, 5, 2)  # B - F, weight 2
    g.add_edge(6, 5, 5)  # G - F, weight 5
    g.add_edge(6, 8, 4)  # G - I, weight 4
    g.add_edge(6, 7, 5)  # G - H, weight 5
    g.add_edge(8, 9, 2)  # I - J, weight 2

    # Running the Bellman-Ford algorithm from D to all vertices
    print("\nThe Bellman-Ford Algorithm starting from vertex D to F:")
    negative_cycle, distances, predecessors = g.bellman_ford('D', 'F')
    g.show_path_from_src_to_dest(negative_cycle, distances, predecessors)

    print('\n\n')

