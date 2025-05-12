from parse import Parser        # Importamos librerias

if __name__ == '__main__':      # Ejecutamos todos los metodos 
    texto = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6"     # 
    parser = Parser(texto)
    partida = parser.parse(texto)
    print(partida)
