from parser import ParserSAN       # Importamos librerias

def get_san_from_user() -> str:
    """
    Permite al usuario ingresar los movimientos en SAN.
    El usuario puede ingresar varias líneas; para finalizar, ingrese una línea vacía.
    """
    print("Introduce los movimientos de la partida en notación SAN.")
    lineas = []
    while True:
        linea = input()
        if linea.strip() == "":
            break
        lineas.append(linea.strip())
    # Unir todas las líneas con espacios
    return ' '.join(lineas)
print("""
| ¡BIENVENIDO AL CHISMOSO DE PARTIDAS DE AJEDREZ! |
| DESCRIPCIÓN | Este modelo te ayuda a validar partidas en notación SAN. |
""")
# Obtener SAN del usuario
texto = get_san_from_user()
parser = ParserSAN(texto)
try:
        partida = parser.parse()
        print("Partida parseada correctamente:")
        print(partida)
except ValueError as e:
        print(f"Error al parsear la partida: {e}")
