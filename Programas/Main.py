from parser import ParserSAN
from visualizador import VisualizadorAjedrez

def obtener_san_usuario():
    
    print("""\n| INSTRUCCIONES | Ingrese la partida en notación SAN (ej: 1. e4 e5 2. Nf3 Nc6)""")
    print("| Cuando termines, presiona Enter dos veces\n")
    
    lineas = []
    while True:

        linea = input("Ingrese línea de movimientos: ").strip()
        if not linea:
            break
        lineas.append(linea)
    
    return ' '.join(lineas)

def main():
    # Creamos un mensaje default
    print("""| ¡BIENVENIDO AL CHISMOSO DE PARTIDAS DE AJEDREZ! | \n| DESCRIPCIÓN | Este es un modelo avanzado en Chismografia que te sapea si hicieron Trampa \no la Cagaron en una partida de Ajedrez. Tu solo encargate de darle el SAN de la Partida al \nChismoso, que este te guiara a la luz |""")          
    
    try:
        # 1. Obtener entrada
        texto = obtener_san_usuario()
        
        # 2. Parsear
        print(f"| ALERTA | Inicializando parseado y verificacion de Partida |\n| Analizando partida...")
        
        parser = ParserSAN(texto)
        partida = parser.parse()
        movimientos = parser.obtenerElementos()
        print(f"\n| ALERTA | Partida procesada exitosamente: {partida} \n| INFO | No es por afirma ni por confirmar pero, \n no hubo ningun error o movimiento ilegal encontrado")
        
        # 3. Visualizar
        visor = VisualizadorAjedrez(partida, movimientos)
        visor.mostrar_arbol()
        
    except Exception as e:
        print(f"\n| ERROR | {str(e)}")

if __name__ == "__main__":
    main()
