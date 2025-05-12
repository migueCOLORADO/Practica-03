from Parser import Parser

if __name__ == '__main__':
    texto = '1. e4 e5 2. Nf3 Nc6 3. Bb5 a6'
    parser = Parser(texto)
    partida = parser.parse()
    print(partida)
