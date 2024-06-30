import matplotlib.pyplot as plt
import networkx as nx
from torch_geometric.utils import to_networkx
import torch

''' working but the visualization graph is not correct '''

def visualization_engine(data):
    G = nx.Graph()
    user_nodes = data['user'].x
    for i in range(len(user_nodes)):
        G.add_node(f'user_{i}', node_type='user', features=user_nodes[i].numpy())
    movie_nodes = data['movie'].x
    for i in range(len(movie_nodes)):
        G.add_node(f'movie_{i}', node_type='movie', features=movie_nodes[i].numpy())

    edge_index = data['user', 'rates', 'movie'].edge_index
    for i in range(edge_index.size(1)):
        user_idx = edge_index[0, i].item()
        movie_idx = edge_index[1, i].item()
        G.add_edge(f'user_{user_idx}', f'movie_{movie_idx}')

    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)

    user_nodes = [n for n, d in G.nodes(data=True) if d['node_type'] == 'user']
    movie_nodes = [n for n, d in G.nodes(data=True) if d['node_type'] == 'movie']

    nx.draw_networkx_nodes(G, pos, nodelist=user_nodes, node_color='blue', label='Users', node_size=50)
    nx.draw_networkx_nodes(G, pos, nodelist=movie_nodes, node_color='green', label='Movies', node_size=50)

    nx.draw_networkx_edges(G, pos, alpha=0.5)

    plt.legend()
    plt.title('User-Item Graph Visualization')
    plt.show()

data = torch.load('/home/satvik/nax/NAX/graphs/movie_lens_1m.pt')
visualization_engine(data)
