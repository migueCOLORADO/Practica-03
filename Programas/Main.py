from parser import Parser

def main():
    texto = input("Ingrese la partida en notacion SAN: ")
    parser = Parser(texto)
    try:
        partida = parser.parse()
        print("Partida parseada correctamente:")
        print(partida)
    except ValueError as e:
        print(f"Error al parsear la partida: {e}")

if __name__ == '__main__':
    main()

