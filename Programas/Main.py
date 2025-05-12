from parser import ParserSAN       # Importamos librerias

def get_san_from_user() -> str:
    print("""
| ¡BIENVENIDO AL CHISMOSO DE PARTIDAS DE AJEDREZ! |
| DESCRIPCIÓN | Este es un modelo avanzado en Chismografia que te sapea si hicieron Trampa \n
o la Cagaron en una partida de Ajedrez. Tu solo encargate de darle el SAN de la Partida al \n
Chismoso, que este te guiara a la luz|""")
    
    lineas = []
    while True:
        linea = input("""| Ingreso de la descripcion SAN de la Partida: """)
        print(f"Si ya ingreso el SAN, dele click 2 veces a la tecla 'Enter' ")
        
        if linea.strip() == "":
            break
        
        lineas.append(linea.strip())
    # Unir todas las líneas con espacios
    return ' '.join(lineas)


# Obtener SAN del usuario
texto = get_san_from_user()
parser = ParserSAN(texto)
try:
        partida = parser.parse()
        print(f"La partida fue parseada correctamente: {partida}")
except ValueError as e:
        print(f"Error al parsear la partida: {e}")