from parser import ParserSAN
from visualizador import VisualizadorAjedrez

def obtener_san_usuario():
    lineas = []
    # Primera lectura con prompt explícito
    primera = input().strip()
    if primera:
        lineas.append(primera)

    # Luego, solo lecturas “silenciosas” hasta línea vacía
    while True:
        linea = input().strip()
        if not linea:
            break
        lineas.append(linea)

    return ' '.join(lineas)

def main():
    texto = obtener_san_usuario()
    parser = ParserSAN(texto)
    partida = parser.parse()
    movimientos = parser.obtenerElementos()

    visor = VisualizadorAjedrez(partida, movimientos)
    visor.mostrar_arbol()

if __name__ == "__main__":
    main()
