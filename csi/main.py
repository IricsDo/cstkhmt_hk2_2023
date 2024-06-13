from community import community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import graph.build_graph as bgraph
import randomcolor

def louvain_method(G: nx.Graph):
    # load the karate club graph
    # G = nx.karate_club_graph()

    # compute the best partition
    partition = community_louvain.best_partition(G)
    print("Number of community louvain", len(list(set(partition.values()))))
    # draw the graph
    pos = nx.spring_layout(G, seed=42, k = 0.3)
    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    im = nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=12, 
                        cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")
    title = f"Found in louvain {len(list(set(partition.values())))} community"
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    # plt.show()
    plt.savefig("csi/visualize/Louvain.png")
    plt.clf()

def girvan_newman_method(G: nx.Graph):
    # Load karate graph and find communities using Girvan-Newman
    # G = nx.karate_club_graph()
    communities = list(nx.community.girvan_newman(G))

    # Modularity -> measures the strength of division of a network into modules
    modularity_df = pd.DataFrame(
        [
            [k + 1, nx.community.modularity(G, communities[k])]
            for k in range(len(communities))
        ],
        columns=["k", "modularity"],
    )

    fig, ax = plt.subplots(3, figsize=(15, 20))

    # Plot graph with colouring based on communities
    visualize_communities(G, communities[0], 1)
    visualize_communities(G, communities[3], 2)

    # Plot change in modularity as the important edges are removed
    modularity_df.plot.bar(
        x="k",
        ax=ax[2],
        color="#F2D140",
        title="Modularity Trend for Girvan-Newman Community Detection",
    )
    # plt.show()
    plt.savefig("csi/visualize/Girvan-Newman.png")
    plt.clf()

# function to create node colour list
def create_community_node_colors(graph, communities):
    colors  = [randomcolor.RandomColor().generate()[0] for _ in range(100)]
    colors = list(set(colors))
    node_colors = []
    for node in graph:
        current_community_index = 0
        for community in communities:
            if node in community:
                node_colors.append(colors[current_community_index])
                break
            current_community_index += 1
    return node_colors


# function to plot graph with node colouring based on communities
def visualize_communities(graph, communities, i):
    node_colors = create_community_node_colors(graph, communities)
    modularity = round(nx.community.modularity(graph, communities), 6)
    title = f"Community Visualization of {len(communities)} communities with modularity of {modularity}"
    pos = nx.spring_layout(graph, k=0.3, iterations=50, seed=42)
    plt.subplot(3, 1, i)
    plt.title(title)
    nx.draw(
        graph,
        pos=pos,
        node_size=40,
        node_color=node_colors,
        with_labels=False,
        font_size=20,
        font_color="black",
    )

if __name__ == '__main__':

    G = bgraph.load_graph_0()
    louvain_method(G)
    girvan_newman_method(G)
    exit(0)