import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

n = 6

X = np.random.random_integers(0, 1, (n,n))
for i in range(n):
    X[i][i]=0

print(X)

G = nx.DiGraph()

# Add nodes
for i in range(n):
    G.add_node(i, label=f"Company {i+1}")

# Add edges based on investment matrix
for i in range(n):
    for j in range(n):
        if X[i][j] == 1:
            G.add_edge(i, j)


# Draw the graph
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx_nodes(G, pos, node_color='pink', node_size=1000)
nx.draw_networkx_labels(G, pos, labels={i: f"Company {i+1}" for i in range(n)}, font_size=12)

for u, v in G.edges():
    if G.has_edge(v, u):  # Bidirectional
        color = 'purple'
    else:  # Unidirectional
        color = 'gray'
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width = 3, arrowstyle='-|>',arrowsize=40, edge_color=color)


plt.title("n=6", fontsize=20)
#plt.key()
plt.show()
