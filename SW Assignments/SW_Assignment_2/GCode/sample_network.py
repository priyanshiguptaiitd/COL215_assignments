import networkx as nx

import matplotlib.pyplot as plt

G = nx.petersen_graph()
y = nx.algorithms.community.louvain_communities(G)
nx.draw(G, with_labels=True)
plt.show()
print(y)