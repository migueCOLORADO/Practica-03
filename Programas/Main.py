from parser import ParserSAN       # Importamos librerias

if __name__ == '__main__':      # Ejecutamos todos los metodos
    print(f"""| ¡BIENVENIDO AL CHISMOSO DE PARTIDAS DE AJEDREZ! | \n
| DESCRIPCION | Este es un modelo de Chismografia avanzado que te sapea si se hizo Trampa \n
o la Cagaron en una partidad de Ajedrez. Tu solo encargate de darle el SAN de la partida al \n
Chismoso y el te guiara a la luz...
""")
    
    texto = str(input("Ingrese el SAN de la Partida de Ajedrez: "))
<<<<<<< Updated upstream
    texto = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6" 
    parser = ParserSAN(texto)
=======
    parser = Parser(texto)
>>>>>>> Stashed changes
    partida = parser.parse(texto)
    print(partida)
