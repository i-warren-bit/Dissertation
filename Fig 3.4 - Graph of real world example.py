import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


countries = ["Canada", "Germany", "France", "UK", "Italy", "US"]

# Your matrix (rows = creditors, columns = borrowers)
C = [
    [0.000, 0.008, 0.010, 0.052, 0.001, 0.135],
    [0.040, 0.000, 0.080, 0.049, 0.059, 0.031],
    [0.056, 0.084, 0.000, 0.075, 0.214, 0.052],
    [0.044, 0.061, 0.137, 0.000, 0.013, 0.112],
    [0.004, 0.071, 0.041, 0.011, 0.000, 0.004],
    [0.189, 0.110, 0.065, 0.147, 0.047, 0.000]
]


G = nx.DiGraph()

for country in countries:
    G.add_node(country)

node_sizes = [
    456830.755,
    1092046.449,
    1069069.289,
    1357195.064,
    665099.338,
    5382588.912
]

scaled_sizes = [x**0.5 for x in node_sizes]

# Add edges (borrower -> creditor)
for i, creditor in enumerate(countries):
    for j, borrower in enumerate(countries):
        weight = C[i][j]
        if weight > 0.05:
            G.add_edge(borrower, creditor, weight=weight)

# Layout
pos = nx.spring_layout(G, seed=47)


# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=scaled_sizes, node_color='lightblue')

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=8)

# Draw edges with thickness proportional to weights
edges = G.edges(data=True)
weights = [d['weight'] * 10 for (_, _, d) in edges]  # scale for visibility

nx.draw_networkx_edges(G, pos, width=weights , edge_color='blue')
# Draw edges as faint lines (no arrows)
#nx.draw_networkx_edges(G, pos, alpha=0.3)

for u, v, d in G.edges(data=True):
    x1, y1 = pos[u]
    x2, y2 = pos[v]

    rad = 0.05 if u < v else -0.05

    # interpolate points (move inward toward center)
    t1, t2 = 0.6, 0.8
    xm1, ym1 = x1 + t1 * (x2 - x1), y1 + t1 * (y2 - y1)
    xm2, ym2 = x1 + t2 * (x2 - x1), y1 + t2 * (y2 - y1)

    arrow = FancyArrowPatch(
        (xm1, ym1), (xm2, ym2),
        #connectionstyle=f"arc3,rad={rad}",
        arrowstyle='-|>',
        mutation_scale=15,
        linewidth=d['weight'] * 5,
        color='blue'
    )

    plt.gca().add_patch(arrow)


# Draw edge labels (optional, can be cluttered)
edge_labels = {(u, v): f"{d['weight']:.3f}" for u, v, d in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, connectionstyle='arc3,rad=0.1', label_pos=0.65)

plt.title("Directed Weighted Network Graph of Cross-Holdings of 6 countries")
plt.axis('off')
plt.show() 