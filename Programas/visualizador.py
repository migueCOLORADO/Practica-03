import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button
import re

class VisualizadorAjedrez:
    def __init__(self, partida, movimientos):
        self.partida = partida
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.setup_ui()
        self.node_positions = {}
        self.movimientos = movimientos

    def setup_ui(self):
        plt.subplots_adjust(bottom=0.15)
        self.ax_zoom_in = plt.axes([0.2, 0.05, 0.15, 0.075])
        self.ax_zoom_out = plt.axes([0.4, 0.05, 0.15, 0.075])
        self.ax_reset = plt.axes([0.6, 0.05, 0.15, 0.075])
        
        self.btn_zoom_in = Button(self.ax_zoom_in, 'Zoom In (+)')
        self.btn_zoom_out = Button(self.ax_zoom_out, 'Zoom Out (-)')
        self.btn_reset = Button(self.ax_reset, 'Reset View')
        
        self.btn_zoom_in.on_clicked(self.zoom_in)
        self.btn_zoom_out.on_clicked(self.zoom_out)
        self.btn_reset.on_clicked(self.reset_view)

    def zoom_in(self, event):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0]*0.8, xlim[1]*0.8)
        self.ax.set_ylim(ylim[0]*0.8, ylim[1]*0.8)
        plt.draw()

    def zoom_out(self, event):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0]*1.2, xlim[1]*1.2)
        self.ax.set_ylim(ylim[0]*1.2, ylim[1]*1.2)
        plt.draw()

    def reset_view(self, event):
        all_x = [pos[0] for pos in self.node_positions.values()]
        all_y = [pos[1] for pos in self.node_positions.values()]
        padding = 1
        self.ax.set_xlim(min(all_x)-padding, max(all_x)+padding)
        self.ax.set_ylim(min(all_y)-padding, max(all_y)+padding)
        plt.draw()

    def mostrar_arbol(self):
        print(f"\n| ALERTA | Creando interfaz grafica...")
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
        mov_idx = 0  # Índice para movimientos
        
        for turno in self.partida.turnos:
            new_parents = []
            
            if mov_idx >= len(listMovimientos):
                break
                
            for parent in parent_nodes:
                # Jugada blanca (siempre existe)
                if mov_idx < len(listMovimientos):
                    blanca_node = f"JUGADA {mov_idx}\n{listMovimientos[mov_idx]}"
                    G.add_node(blanca_node, tipo="blanca", nivel=nivel_actual)
                    G.add_edge(parent, blanca_node)
                    new_parents.append(blanca_node)
                    mov_idx += 1
                    
                    # Jugada negra (si existe)
                    if turno.negra and mov_idx < len(listMovimientos):
                        negra_node = f"JUGADA {mov_idx}\n{listMovimientos[mov_idx]}"
                        G.add_node(negra_node, tipo="negra", nivel=nivel_actual)
                        G.add_edge(parent, negra_node)
                        new_parents.append(negra_node)
                        mov_idx += 1
            
            parent_nodes = new_parents
            nivel_actual += 1
        
        # Calcular posiciones
        self.calculate_positions(G)
        
        # Dibujar el árbol
        print(f"| ALERTA | Generando Arbol Binario para: {listMovimientos}")
        print(f"\n| INFO | Gracias por nutrir al arte de la comunicacion de eventos microhistoricos...\n| En fin, deje el chisme que es perjudicial para la salud - Att: El Chismoso")
        self.draw_tree(G)
        plt.show()

    def calculate_positions(self, G):
        # Primero agrupar nodos por nivel
        niveles = {}
        for node in G.nodes():
            nivel = G.nodes[node].get("nivel", 0)
            if nivel not in niveles:
                niveles[nivel] = []
            niveles[nivel].append(node)
        
        # Asignar posiciones
        for nivel in sorted(niveles.keys()):
            nodos = niveles[nivel]
            y = -nivel * 2
            
            # Espaciado horizontal según nivel
            width = 2 ** (nivel - 1) if nivel > 0 else 1
            x_start = -width
            step = (width * 2) / (len(nodos) - 1) if len(nodos) > 1 else 0
            
            for i, node in enumerate(nodos):
                self.node_positions[node] = (x_start + i * step, y)

    def draw_tree(self, G):
        self.ax.clear()
        
        # Colores según tipo de nodo
        node_colors = []
        for node in G.nodes():
            if node == "Partida":
                node_colors.append('gold')
            elif G.nodes[node].get("tipo") == "blanca":
                node_colors.append('white')
            else:
                node_colors.append('lightgray')
        
        # Dibujar aristas
        nx.draw_networkx_edges(G, self.node_positions, ax=self.ax, 
                              arrows=False, width=1.2, edge_color='gray')
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, self.node_positions, ax=self.ax,
                             node_color=node_colors, node_size=1500,
                             edgecolors='black')
        
        # Etiquetas con formato
        labels = {}
        for node in G.nodes():
            if node == "Partida":
                labels[node] = node
            else:
                parts = node.split('\n')
                labels[node] = f"{parts[0]}\n{parts[1]}"
        
        nx.draw_networkx_labels(G, self.node_positions, labels, 
                              font_size=9, ax=self.ax)
        
        # Configuración final
        self.ax.set_title("Árbol Binario de Partida de Ajedrez", pad=20, fontsize=14)
        self.ax.axis('off')
        self.fig.subplots_adjust(
            left=0.05,
            right=0.95,
            top=0.9,
            bottom=0.2  # Ajusta según el tamaño de tus botones
        )
