# Interfaz.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from parser import ParserSAN
from visualizador import VisualizadorAjedrez

class Interfaz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador de Partidas de Ajedrez")
        self.setFixedSize(1600, 1000)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Mensaje de bienvenida
        bienvenida = QLabel("¡Bienvenido al analizador de partidas de ajedrez!")
        bienvenida.setFont(QFont("Arial", 16))
        bienvenida.setAlignment(Qt.AlignCenter)
        layout.addWidget(bienvenida)

        # Instrucción explicativa
        instruccion = QLabel("Ingrese la partida de ajedrez en notación SAN (ej: 1. e4 e5 2. Nf3 Nc6)")
        instruccion.setAlignment(Qt.AlignCenter)
        instruccion.setFont(QFont("Arial", 11))
        layout.addWidget(instruccion)

        # Caja de entrada de texto
        self.campo_san = QLineEdit()
        self.campo_san.setPlaceholderText("Ingrese la partida")
        self.campo_san.setFixedHeight(40)
        self.campo_san.setFont(QFont("Arial", 12))
        layout.addWidget(self.campo_san)

        layout.addSpacing(20)

        # Botones horizontalmente
        botones_layout = QHBoxLayout()

        btn_salir = QPushButton("Salir")
        btn_salir.setStyleSheet("background-color: red; color: white;")
        btn_salir.setFixedSize(100, 40)
        btn_salir.clicked.connect(self.close)

        btn_analizar = QPushButton("Analizar")
        btn_analizar.setStyleSheet("background-color: blue; color: white;")
        btn_analizar.setFixedSize(100, 40)
        btn_analizar.clicked.connect(self.analizar_partida)

        botones_layout.addWidget(btn_salir)
        botones_layout.addSpacing(40)
        botones_layout.addWidget(btn_analizar)

        layout.addLayout(botones_layout)

        # Canvas de Matplotlib para mostrar el árbol
        self.canvas = FigureCanvas(plt.figure(figsize=(16, 10)))
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.canvas)
        layout.setStretch(layout.count() - 1, 1)

        self.setLayout(layout)

    def analizar_partida(self):
        texto_partida = self.campo_san.text().strip()

        if not texto_partida:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese una partida.")
            return

        try:
            parser = ParserSAN(texto_partida)
            partida = parser.parse()
            movimientos = parser.obtenerElementos()

            # Limpiar canvas y dibujar el árbol
            self.canvas.figure.clf()
            ax = self.canvas.figure.add_subplot(111)
            viz = VisualizadorAjedrez(partida, movimientos, fig=self.canvas.figure, ax=ax)
            viz.mostrar_arbol()
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error en la partida", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Interfaz()
    ventana.show()
    sys.exit(app.exec_())
