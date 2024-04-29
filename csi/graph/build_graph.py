import pandas
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def load_graph_1():
    df = pandas.read_csv('csi/data/gene_fusion/out.gene_fusion.csv')
    df.rename(columns={'% sym unweighted': 'point1', 'Unnamed: 1': 'point2'}, inplace=True)
    point1 = df['point1'].tolist()
    point2 = df['point2'].tolist()

    if len(point1) != len(point2):
        raise 'Exception in data'
    
    G = nx.Graph()

    for i in range(len(point1)):
        G.add_edge(point1[i], point2[i])

    print('Edges:', G.number_of_edges())
    print('Nodes:', G.number_of_nodes())
    
    pos = nx.spring_layout(G, seed=42, k=0.3)

    nx.draw(G, pos, with_labels = False, width=0.4, node_color='black', node_size=len(point1)/2)
    plt.savefig("csi/visualize/gen_fusion_spring1.png")
    plt.clf()

    return G

def load_graph_0():
    df = pandas.read_csv('csi/refer/konect-extr-master/extr/pholme/gene_fusion.csv', names=['point1', 'point2'])
    df= df.iloc[1:, :]
    point1 = df['point1'].astype(int).tolist()
    point2 = df['point2'].astype(int).tolist()

    if len(point1) != len(point2):
        raise 'Exception in data'
    
    G = nx.Graph()

    for i in range(len(point1)):
        G.add_edge(point1[i], point2[i])

    print('Edges:', G.number_of_edges())
    print('Nodes:', G.number_of_nodes())
    
    pos = nx.spring_layout(G, seed=42, k = 0.3)

    nx.draw(G, pos, with_labels = False, width=0.4, node_color='black', node_size=len(point1)/2)
    plt.savefig("csi/visualize/gen_fusion_spring0.png")
    plt.clf()

    return G

if __name__ == '__main__':

    load_graph_1()
    load_graph_0()

    exit(0)