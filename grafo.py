import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos al grafo
G.add_node(1)
G.add_node(2)
G.add_node(3)

# Agregar aristas al grafo
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)

# Dibujar el grafo
plt.figure(figsize=(8, 5))
nx.draw(G, with_labels=True, font_weight='bold', node_color='skyblue', font_size=16, node_size=700)
plt.title("Grafo Dirigido")
plt.show()
