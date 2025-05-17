# visualizador.py
import matplotlib.pyplot as plt
import networkx as nx
import re

class VisualizadorAjedrez:
    def __init__(self, partida, movimientos, fig=None, ax=None):
        self.partida = partida
        self.node_positions = {}
        self.movimientos = movimientos
        if fig is not None:
            self.fig = fig
            if ax is not None:
                self.ax = ax
            else:
                self.ax = fig.add_subplot(111)
        else:
            self.fig, self.ax = plt.subplots(figsize=(20, 15))
        # Fondo completamente blanco
        self.fig.patch.set_facecolor('white')
        self.ax.set_facecolor('white')

    def mostrar_arbol(self):
        G = nx.DiGraph()
        # Nodo raíz
        G.add_node("Partida", tipo="raiz", nivel=0)
        self.node_positions["Partida"] = (0, 0)
        # Procesar movimientos correctamente
        listMovimientos = [mov for mov in re.sub(r'\d+\.', '', self.movimientos).split() if mov]
        print(f"| INFO | Movimientos procesados: {listMovimientos}")
        # Construcción del árbol
        parent_nodes = ["Partida"]
        nivel_actual = 1
        mov_idx = 0
        for turno in self.partida.turnos:
            new_parents = []
            if mov_idx >= len(listMovimientos):
                break
            for parent in parent_nodes:
                # Jugada blanca (siempre existe)
                if mov_idx < len(listMovimientos):
                    blanca_node = listMovimientos[mov_idx]
                    G.add_node(blanca_node, tipo="blanca", nivel=nivel_actual)
                    G.add_edge(parent, blanca_node)
                    new_parents.append(blanca_node)
                    mov_idx += 1
                # Jugada negra (si existe)
                if turno.negra and mov_idx < len(listMovimientos):
                    negra_node = listMovimientos[mov_idx]
                    G.add_node(negra_node, tipo="negra", nivel=nivel_actual)
                    G.add_edge(parent, negra_node)
                    new_parents.append(negra_node)
                    mov_idx += 1
            parent_nodes = new_parents
            nivel_actual += 1
        # Calcular posiciones (ajustado para mejor espaciado)
        self.calculate_positions(G)
        # Dibujar el árbol
        self.draw_tree(G)

    def calculate_positions(self, G):
        # Primero agrupar nodos por nivel
        niveles = {}
        for node in G.nodes():
            nivel = G.nodes[node].get("nivel", 0)
            if nivel not in niveles:
                niveles[nivel] = []
            niveles[nivel].append(node)
        # Espaciado horizontal
        x_spacing = 5  # Espacio horizontal entre nodos
        y_spacing = 2  # Espacio vertical entre niveles
        for nivel, nodos in niveles.items():
            n_nodos = len(nodos)
            total_width = (n_nodos - 1) * x_spacing
            x_start = -total_width / 2 if n_nodos > 1 else 0
            y = -nivel * y_spacing
            for i, node in enumerate(nodos):
                self.node_positions[node] = (x_start + i * x_spacing, y)

    def draw_tree(self, G):
        self.ax.clear()
        # Colores según tipo de nodo
        node_colors = []
        node_edgecolors = []
        for node in G.nodes():
            if node == "Partida":
                node_colors.append('gold')
                node_edgecolors.append('black')
            elif G.nodes[node].get("tipo") == "blanca":
                node_colors.append('white')
                node_edgecolors.append('orange')
            else:
                node_colors.append('darkgray')
                node_edgecolors.append('black')
        # Dibujar aristas (líneas rectas)
        nx.draw_networkx_edges(G, self.node_positions, ax=self.ax,
                               arrows=False, width=2, edge_color='black')
        # Dibujar nodos (círculos)
        nx.draw_networkx_nodes(G, self.node_positions, ax=self.ax,
                               node_color=node_colors, node_size=800,
                               edgecolors=node_edgecolors, linewidths=2)
        # Etiquetas (solo las jugadas)
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, self.node_positions, labels,
                                font_size=10, font_color='black', ax=self.ax)
        # Configuración final
        self.ax.set_title("Árbol Binario de Partida de Ajedrez", pad=20, fontsize=14)
        self.ax.axis('off')
        self.fig.tight_layout()
